from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import path
import jsonschema
import json
import importlib
import sys
from .endpoints import openapi, OperationId


PATH_START = "api/"


def path_from_operation_id(id):
    for openapi_path, method_definition in openapi["paths"].items():
        for operation in method_definition.values():
            operationId = OperationId(operation["operationId"])
            slug = "{}{}".format(operationId.name(), operationId.variant())
            spec = importlib.util.spec_from_file_location(
                slug, "./parttobe/openapiviews/{}.py".format(slug)
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[slug] = module
            loaded = spec.loader.exec_module(module)
            validator = getattr(module, "validate")
            handler = getattr(module, "handle")
            if operationId.name() == id:
                return path(
                    openapi_path.replace("/" + PATH_START, ""),
                    unmarshaler(handler, validator),
                    name=id,
                )


def is_request_body_required(definition):
    return "requestBody" in definition and (
        "required" not in definition["requestBody"]
        or definition["requestBody"]["required"]
    )


def get_request_body_schema(definition):
    return definition["requestBody"]["content"]["application/json"]["schema"]


def get_definition(request):
    path = request.path
    try:
        return openapi["paths"][path][request.method.lower()]
    except KeyError:
        pass


def unmarshal(request):
    """the request has already been openapi validated"""
    definition = get_definition(request)
    response = {}
    if request.body:
        body = json.loads(request.body)
        response |= body
    return response


def validate(request):
    definition = get_definition(request)
    if not definition:
        return Response({"message": "Path not defined"}, 404)
    if is_request_body_required(definition):
        body = json.loads(request.body)
        try:
            jsonschema.validate(
                instance=body, schema=get_request_body_schema(definition)
            )
        except jsonschema.ValidationError as e:
            return Response({"message", e.message}, 400)


def unmarshaler(implementation, validator):
    @api_view(["GET", "POST"])
    def handle_request(request):
        validation = validate(request)
        arguments = unmarshal(request)
        if validation:
            return validation
        application_validation = validator and validator(**arguments)
        if application_validation:
            return Response(application_validation, 400)
        return Response(implementation(**arguments))

    return handle_request
