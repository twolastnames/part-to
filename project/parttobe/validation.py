from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import path
import django.core.exceptions as exceptions
import jsonschema
import json
import importlib
import sys
import os
import re
from . import models
from .endpoints import (
    openapi,
    OperationId,
    implementation_filename,
    definition_filename,
    traverse_api,
    map_tree,
    global_status_codes,
)
from uuid import uuid4, UUID
from string import ascii_lowercase, ascii_uppercase

PATH_START = "api/"


class ResourceError(RuntimeError):
    def __init__(self, message):
        self.message = message

class ValidationError(RuntimeError):
    def __init__(self, message):
        self.message = message


letter_to_number = {}
number_to_letter = {}

for index, letter in enumerate(
    "".join([str(number) for number in range(10)])
    + ascii_lowercase
    + ascii_uppercase
):
    letter_to_number[letter] = index
    number_to_letter[index] = letter


def shorten_uuid(value):
    current = UUID(str(value)).int
    shortened = ""
    while True:
        if current < len(number_to_letter):
            return shortened + number_to_letter[current]
        remainder = current % len(number_to_letter)
        shortened += number_to_letter[remainder]
        current = current // len(number_to_letter)


def recover_uuid(value):
    current = 0
    for index, digit in enumerate(value):
        reversed_index = len(letter_to_number) - index
        if digit == "-":
            continue
        current += (
            len(letter_to_number) ** index * letter_to_number[digit]
        )
    return UUID(int=current)


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

def handle_id_type(value, format):
    if hasattr(value, 'uuid'):
        return shorten_uuid(value.uuid)
    return shorten_uuid(value)

def map_value(value, schema):
    if "format" in schema and schema['format'].endswith('Id'):
        return handle_id_type(value, schema['format'])
    elif "format" in schema:
        type = schema["format"]
    else:
        type = schema["type"]
    if type == "date-time":
        return value.isoformat()
    elif type == "uuid":
        return shorten_uuid(value)
    return value


def have_marshaled_bodies(operation):
    return {
        status: lambda raw_body: Response(
            map_tree(
                map_value,
                response["content"]["*"]["schema"],
                raw_body,
            ),
            status,
        )
        for status, response in operation["responses"].items()
        if status not in global_status_codes
    }


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
            definition = definition_filename(operationId)
            if not (
                os.path.isfile(filename)
                and os.path.isfile(definition)
            ):
                return path(
                    openapi_path.replace("/" + PATH_START, ""),
                    undefined_path,
                    name=id,
                )
            if operationId.name() == id:
                partial_path = openapi_path.replace(
                    "/" + PATH_START, ""
                )
                variants[operationId.variant().upper()] = {
                    "handle": get_meta_definition(filename, "handle"),
                    "responders": have_marshaled_bodies(
                        operation,
                    ),
                    "argumentType": get_meta_definition(
                        definition, "arguments"
                    ),
                }
    return path(
        partial_path,
        unmarshaler(variants),
        name=id,
    )


def is_request_body_required(definition):
    return "requestBody" in definition and (
        "required" not in definition["requestBody"]
        or definition["requestBody"]["required"]
    )


def are_request_parameters_required(definition):
    return "parameters" in definition and (
        "required" not in definition["parameters"]
        or definition["parameters"]["required"]
    )


def get_request_body_schema(definition):
    return definition["requestBody"]["content"]["*"]["schema"]


def get_definition(request):
    path = request.path
    try:
        return openapi["paths"][path][request.method.lower()]
    except KeyError:
        pass


loaded_model_definitions = {}


def add_loadable_model_definition(name):
    self_directory = os.path.dirname(os.path.abspath(__file__))
    model_filename = os.path.join(self_directory, "models.py")
    definition_name = re.sub(r"Id$", "", name)
    exec(
        "loaded_model_definitions[name] = models.{}".format(
            definition_name
        )
    )


def get_model_uuid_constructor(name):
    def construct_model(wire_uuid):
        if name not in loaded_model_definitions:
            add_loadable_model_definition(name)
        print("wire_uuid", wire_uuid)
        try:
            return loaded_model_definitions[name].objects.get(
                uuid=recover_uuid(wire_uuid)
            )
        except exceptions.ObjectDoesNotExist:
            raise ResourceError("Id {} does not exist".format(wire_uuid))
    return construct_model


unmarshal_parameter_handlers = {
    "string": lambda value: value,
    "uuid": recover_uuid,
    "number": int,
    "date-time": lambda value: datetime.datetime.fromisoformat(value),
} | {
    type: get_model_uuid_constructor(type)
    for type in set(
        [
            format
            for format in traverse_api(lambda key: key == "format")
            if format.endswith("Id")
        ]
    )
}


def unmarshal(request):
    """the request has already been openapi validated"""
    definition = get_definition(request)
    response = {}
    if request.body:
        body = json.loads(request.body)
        response |= body
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
        if type not in unmarshal_parameter_handlers:
            raise ValidationError(
                "Format of type {} not defined in schema".format(type)
            )
        print("value", parameter, value)
        response[parameter["name"]] = unmarshal_parameter_handlers[
            type
        ](value)
    return response


def is_parameter_correct(request, parameter):
    if "default" in parameter:
        value = request.GET.get(
            parameter["name"],
            parameter["default"],
        )
    else:
        value = request.GET.get(parameter["name"])
    type = parameter["schema"]["type"]
    if type == "string":
        return True
    if type == "number":
        try:
            int(value)
            return True
        except ValueError:
            return False
    raise NotImplementedError("Parameter Type".format(type))


def get_parameter_errors(request):
    definition = get_definition(request)
    if "parameters" not in definition:
        return []
    errors = [
        error
        for error in map(
            is_parameter_correct,
            definition["paramaters"],
        )
        if error
    ]


def is_valid_body(request):
    definition = get_definition(request)
    if not definition:
        raise ValidationError("Path not defined")
    if not is_request_body_required(definition) and not request.body:
        return
    body = json.loads(request.body)
    try:
        jsonschema.validate(
            instance=body,
            schema=get_request_body_schema(definition),
        )
    except jsonschema.ValidationError as e:
        raise ValidationError(e.message)
    parameter_errors = get_parameter_errors(request)
    if len(parameter_errors) > 0:
        raise ValidationError(parameter_errors)


def validate(request):
    definition = get_definition(request)
    if not definition:
        return Response(
            {"messages": ["Path not defined"]},
            404,
        )
    body_validation_error = is_valid_body(request)
    if body_validation_error:
        return body_validation_error


def unmarshaler(variants):
    @api_view(["GET", "POST"])
    def handle_request(request):
        response = None
        handle = variants[request.method]["handle"]
        responders = variants[request.method]["responders"]
        argumentType = variants[request.method]["argumentType"]
        try:
            validation = is_valid_body(request)
            arguments = unmarshal(request)
        except (exceptions.ValidationError, ResourceError) as e:
            return Response(e.message, status=404)
        except ValidationError as e:
            if isinstance(e.message, list):
                message = e.message
            else:
                message = [e.message]
            return Response(message, status=400)
        for status, responder in responders.items():
            arguments["respond_{}".format(status)] = responders[
                status
            ]
        try:
            response = handle(argumentType(**arguments))
        except (exceptions.ValidationError, ResourceError) as e:
            return Response(e.message, status=404)
        if type(response) is tuple:
            return Response(response)
        if isinstance(response, Response):
            return response
        return Response(response)

    return handle_request
