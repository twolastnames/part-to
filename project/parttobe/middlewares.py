from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .endpoints import operation_paths
from .endpoints import get_definition
from .endpoints import get_request_body_schema
from re import search
import jsonschema
import json


cache_for_path = {}


def set_cache_for_paths(expressions, cache):
    for expression in expressions:
        for operationId, path in operation_paths.items():
            if not search(expression, operationId):
                continue
            cache_for_path[path.strip("/")] = cache


# keep for duration of use
set_cache_for_paths(["metric:get$"], "max-age=10800, must-revalidate")

# keep forever
set_cache_for_paths(
    ["^partto:get$", "^task:get$", "^run.*:get$"],
    "public, max-age=31536000, immutable",
)


class Headers:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/api/"):
            return response
        if request.method.lower() != "get":
            return response
        if request.path.strip("/") in cache_for_path:
            response["Cache-Control"] = cache_for_path[request.path.strip("/")]
        return response


def get_parameter_errors(request):
    definition = get_definition(request)
    return (
        []
        if "parameters" not in definition
        else [
            error
            for error in map(
                get_parameter_error(request),
                definition["parameters"],
            )
            if error
        ]
    )


class ParameterErrorChecker:
    def __init__(self, request):
        self.request = request

    def __call__(self, parameter):
        if "default" in parameter:
            value = self.request.GET.get(
                parameter["name"],
                parameter["default"],
            )
        else:
            value = self.request.GET.get(parameter["name"])
            if not value:
                return "parameter {} missing".format(parameter["name"])
        type = parameter["schema"]["type"]
        if type == "string":
            return
        if type == "number":
            try:
                int(value)
                return
            except ValueError:
                return "expected {} to be parsable to a number".format(
                    parameter["name"]
                )
        raise NotImplementedError("Parameter Type".format(type))


def get_error_response(exception):
    if isinstance(exception, list):
        message = exception
    elif isinstance(exception.message, list):
        message = exception.message
    else:
        message = [exception.message]
    response = Response(data=message, status=400)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response


def is_request_body_required(definition):
    return "requestBody" in definition and (
        "required" not in definition["requestBody"]
        or definition["requestBody"]["required"]
    )


class ApiBodyValidation:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/"):
            return self.get_response(request)
        definition = get_definition(request)
        if not definition:
            return Response("Path not defined", status=404)
        if not is_request_body_required(definition) and not request.body:
            return self.get_response(request)
        try:
            jsonschema.validate(
                instance=json.loads(request.body),
                schema=get_request_body_schema(definition),
            )
        except jsonschema.ValidationError as e:
            return get_error_response(e)
        return self.get_response(request)


class ApiQueryValidation:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/"):
            return self.get_response(request)
        definition = get_definition(request)
        check = ParameterErrorChecker(request)
        parameter_errors = (
            []
            if "parameters" not in definition
            else [
                error
                for error in [
                    check(parameter) for parameter in definition["parameters"]
                ]
                if error
            ]
        )

        if len(parameter_errors) > 0:
            return get_error_response(parameter_errors)
        return self.get_response(request)
