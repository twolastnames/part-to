from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import path
import jsonschema
import json
import importlib
import sys
import os
from .endpoints import openapi, OperationId


PATH_START = "api/"


@api_view(["GET", "POST"])
def undefined_path(request):
    return Response({"messages": ["path '{}' not defined".format(request.path)]}, 500)


def path_from_operation_id(id):
    variants = {}
    partial_path = ""
    for openapi_path, method_definition in openapi["paths"].items():
        for operation in method_definition.values():
            operationId = OperationId(operation["operationId"])
            slug = "{}{}".format(operationId.name(), operationId.variant())
            filename = "./parttobe/openapiviews/{}.py".format(slug)
            if not os.path.isfile(filename):
                return path(
                    openapi_path.replace("/" + PATH_START, ""),
                    undefined_path,
                    name=id,
                )
            spec = importlib.util.spec_from_file_location(slug, filename)
            module = importlib.util.module_from_spec(spec)
            sys.modules[slug] = module
            loaded = spec.loader.exec_module(module)
            validator = getattr(module, "validate")
            handler = getattr(module, "handle")
            if operationId.name() == id:
                partial_path = openapi_path.replace("/" + PATH_START, "")
                variants[operationId.variant().upper()] = {
                    "handler": handler,
                    "validator": validator,
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
    return definition["requestBody"]["content"]["application/json"]["schema"]


def get_definition(request):
    path = request.path
    try:
        return openapi["paths"][path][request.method.lower()]
    except KeyError:
        pass


unmarshal_parameter_handlers = {
    "string": lambda value: value,
    "number": int,
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
            value = request.GET.get(parameter["name"], parameter["default"])
        else:
            value = request.GET.get(parameter["name"])
        type = parameter["schema"]["type"]
        response[parameter["name"]] = unmarshal_parameter_handlers[type](value)
    return response


def is_parameter_correct(request, parameter):
    if "default" in parameter:
        value = request.GET.get(parameter["name"], parameter["default"])
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
        error for error in map(is_parameter_correct, definition["paramaters"]) if error
    ]


def is_valid_body(request):
    definition = get_definition(request)
    if not is_request_body_required(definition) and not request.body:
        return
    body = json.loads(request.body)
    try:
        jsonschema.validate(instance=body, schema=get_request_body_schema(definition))
    except jsonschema.ValidationError as e:
        return Response({"messages", [e.message]}, 400)
    parameter_errors = get_parameter_errors(request)
    if len(parameter_errors) > 0:
        return Response({"messages", parameter_errors}, 400)


def validate(request):
    definition = get_definition(request)
    if not definition:
        return Response({"messages": ["Path not defined"]}, 404)
    body_validation_error = is_valid_body(request)
    if body_validation_error:
        return body_validation_error


def unmarshaler(variants):
    @api_view(["GET", "POST"])
    def handle_request(request):
        validator = variants[request.method]["validator"]
        handler = variants[request.method]["handler"]
        validation = validate(request)
        arguments = unmarshal(request)
        if validation:
            return validation
        application_validation = validator and validator(**arguments)
        if isinstance(application_validation, Response):
            return application_validation
        if application_validation:
            return Response(application_validation, 400)
        response = handler(**arguments)
        if isinstance(response, Response):
            return response
        return Response(response)

    return handle_request