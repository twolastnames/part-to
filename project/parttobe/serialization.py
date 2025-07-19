from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from django.urls import path
import django.core.exceptions as exceptions
import jsonschema
import json
import importlib
import collections
import duration_parser
import datetime
import sys
import os
import re
from . import models
from .endpoints import (
    get_definition,
    openapi,
    OperationId,
    operations,
    implementation_filename,
    definition_filename,
    traverse_api,
    get_request_body_arguments,
    get_parameter_arguments,
    map_tree,
    response_definitions,
)
from uuid import uuid4, UUID
from string import ascii_lowercase, ascii_uppercase

PATH_START = "api/"

automatic_status_returns = ["500"]


class ResourceError(RuntimeError):
    def __init__(self, message):
        self.message = message


class ValidationError(RuntimeError):
    def __init__(self, message):
        self.message = message


@api_view(["GET", "POST"])
def undefined_path(request):
    return Response(
        {"messages": ["path '{}' not defined".format(request.path)]},
        500,
    )


def get_meta_definition(filename, symbol):
    id = "anon_{}".format(uuid4().hex)
    spec = importlib.util.spec_from_file_location(id, filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[id] = module
    loaded = spec.loader.exec_module(module)
    return getattr(module, symbol)


class UuidSerialization(serializers.Field):
    letter_to_number = {}
    number_to_letter = {}

    for index, letter in enumerate(
        "".join([str(number) for number in range(10)])
        + ascii_lowercase
        + ascii_uppercase
    ):
        letter_to_number[letter] = index
        number_to_letter[index] = letter

    def to_representation(self, value):
        current = UUID(str(value)).int
        shortened = ""
        while True:
            if current < len(UuidSerialization.number_to_letter):
                return shortened + UuidSerialization.number_to_letter[current]
            remainder = current % len(UuidSerialization.number_to_letter)
            shortened += UuidSerialization.number_to_letter[remainder]
            current = current // len(UuidSerialization.number_to_letter)

    def to_internal_value(self, data):
        current = 0
        for index, digit in enumerate(data):
            reversed_index = len(UuidSerialization.letter_to_number) - index
            if digit == "-":
                continue
            current += (
                len(UuidSerialization.letter_to_number) ** index
                * UuidSerialization.letter_to_number[digit]
            )
        return UUID(int=current)


class DurationSerialization(serializers.Field):
    def to_representation(self, value):
        return value.total_seconds()

    def to_internal_value(self, data):
        return datetime.timedelta(seconds=data)


class DateTimeSerialization(serializers.Field):
    def to_representation(self, value):
        return value.isoformat()

    def to_internal_value(self, data):
        return datetime.datetime.fromisoformat(data)


def get_model_serialization(name):
    def construct_model(wire_uuid):
        if name not in loaded_model_definitions:
            add_loadable_model_definition(name)
        try:
            return loaded_model_definitions[name].objects.get(
                uuid=UuidSerialization().to_internal_value(wire_uuid)
            )
        except exceptions.ObjectDoesNotExist:
            raise ResourceError("Id {} does not exist".format(wire_uuid))

    class ModelSerialization(serializers.Field):
        def to_representation(self, value):
            return UuidSerialization().to_representation(
                value.uuid if hasattr(value, "uuid") else value
            )

        def to_internal_value(self, data):
            return construct_model(data)

    return ModelSerialization


serialization = {
    "string": serializers.CharField,
    "uuid": UuidSerialization,
    "duration": DurationSerialization,
    "boolean": serializers.BooleanField,
    "integer": serializers.IntegerField,
    "number": serializers.FloatField,
    "date-time": DateTimeSerialization,
} | {
    type: get_model_serialization(type)
    for type in set(
        [
            format
            for format in traverse_api(lambda key: key == "format")
            if format.endswith("Id")
        ]
    )
}


class Serialization:
    def __init__(self, type_schema):
        key = type_schema["format"] if "format" in type_schema else type_schema["type"]
        if key not in serialization:
            raise ValidationError("Format of type {} not defined in schema".format(key))
        self.serialization = serialization[key]

    def to_representation(self, value):
        return self.serialization().to_representation(value)

    def to_internal_value(self, data):
        return self.serialization().to_internal_value(data)


def to_internal_value(data, type_schema):
    return Serialization(type_schema).to_internal_value(data)


def to_representation(value, type_schema):
    return Serialization(type_schema).to_representation(value)


def get_body_serializer(operation):
    for status, response in operation["responses"].items():
        if status != "200":
            continue
        return lambda body: map_tree(
            to_representation,
            response["content"]["*"]["schema"],
            body,
        )
    raise SystemError("operation {} is undefined".format(operation))


class TypeExpansionDoer:
    def __init__(self, operation, operationId):
        self.arguments = list(get_request_body_arguments(operation)) + list(
            get_parameter_arguments(operation)
        )
        self.argument_type = collections.namedtuple(
            "ArgumentType_{}".format(OperationId(operationId).slug()),
            self.arguments,
        )

    def __call__(self, **args):
        return self.argument_type(
            **({key: args.get(key, None) for key in self.arguments})
        )


argument_types = {
    operationId: TypeExpansionDoer(operation, operationId)
    for operationId, operation in operations.items()
}

EndpointVariant = collections.namedtuple(
    "EndpointVariant", "handle serialize argumentType"
)


def path_from_operation_id(id):
    variants = {}
    partial_path = ""
    for (
        openapi_path,
        method_definition,
    ) in openapi["paths"].items():
        for operation in method_definition.values():
            operationId = OperationId(operation["operationId"])
            slug = "{}{}".format(
                operationId.name(),
                operationId.variant(),
            )
            filename = implementation_filename(operationId)
            if not (os.path.isfile(filename)):
                return path(
                    openapi_path.replace("/" + PATH_START, ""),
                    undefined_path,
                    name=id,
                )
            if operationId.name() == id:
                partial_path = openapi_path.replace("/" + PATH_START, "")
                variants[operationId.variant().upper()] = EndpointVariant(
                    handle=get_meta_definition(filename, "handle"),
                    serialize=get_body_serializer(operation),
                    argumentType=argument_types[operationId.value],
                )
    return path(
        partial_path,
        unmarshaler(variants),
        name=id,
    )


loaded_model_definitions = {}


def add_loadable_model_definition(name):
    self_directory = os.path.dirname(os.path.abspath(__file__))
    model_filename = os.path.join(self_directory, "models.py")
    definition_name = re.sub(r"Id$", "", name)
    exec("loaded_model_definitions[name] = models.{}".format(definition_name))


def get_model_uuid_constructor(name):
    def construct_model(wire_uuid):
        if name not in loaded_model_definitions:
            add_loadable_model_definition(name)
        try:
            return loaded_model_definitions[name].objects.get(
                uuid=UuidSerialization().to_internal_value(wire_uuid)
            )
        except exceptions.ObjectDoesNotExist:
            raise ResourceError("Id {} does not exist".format(wire_uuid))

    return construct_model


def unmarshal_value(value, schema):
    return serialization[
        schema["format"] if "format" in schema else schema["type"]
    ]().to_internal_value(value)


def unmarshal(request):
    """the request has already been openapi validated"""
    definition = get_definition(request)
    response = {}
    if request.body:
        body = json.loads(request.body)
        response |= map_tree(
            to_internal_value,
            definition["requestBody"]["content"]["*"]["schema"],
            body,
        )
    if "parameters" not in definition:
        return response
    for parameter in definition["parameters"]:
        if "default" in parameter:
            value = request.GET.get(
                parameter["name"],
                parameter["default"],
            )
        else:
            value = request.GET.get(parameter["name"])

        if "format" in parameter["schema"]:
            type = parameter["schema"]["format"]
        else:
            type = parameter["schema"]["type"]
        if type not in serialization:
            raise ValidationError(
                "Format of type {} not defined in schema".format(type)
            )
        response[parameter["name"]] = Serialization(
            parameter["schema"]
        ).to_internal_value(value)
    return response


def unmarshaler(variants):
    @api_view([value.upper() for value in variants.keys()])
    def handle_request(request):
        response = None
        for_method = variants[request.method]
        try:
            arguments = unmarshal(request)
        except (exceptions.ValidationError, ResourceError) as e:
            return Response({"messages": [e.message]}, status=404)
        try:
            response = for_method.handle(for_method.argumentType(**arguments))
        except (exceptions.ValidationError, ResourceError) as e:
            return Response({"messages": [e.message]}, status=404)
        if isinstance(response, Response):
            return response
        return Response(for_method.serialize(response))

    return handle_request
