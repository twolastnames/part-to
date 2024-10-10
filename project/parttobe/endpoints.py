import os
import yaml
from openapi_core import OpenAPI
import functools


class OperationId:
    def __init__(self, value):
        self.value = value

    def name(self):
        return self.value.split(":")[0].lower()

    def variant(self):
        return self.value.split(":")[1]

    def slug(self):
        return "{}{}".format(self.name(), self.variant())

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def title(self):
        return "{}{}".format(
            self.name().title(), self.variant().title()
        )


class RefInjector:
    def __init__(self, components):
        self.components = components

    def __call__(self, specification):
        if isinstance(specification, dict):
            returnable = {}
            for k, v in specification.items():
                if k != "$ref":
                    returnable[k] = self(v)
                    continue
                parts = v.split("/")[2:]
                schema = functools.reduce(
                    lambda current, next: current[next],
                    parts,
                    self.components,
                )
                returnable |= schema
            return returnable
        if isinstance(specification, list):
            return [self(v) for v in specification]
        else:
            return specification


global_status_codes = ["400", "500"]

self_directory = os.path.dirname(os.path.abspath(__file__))
openapi_filename = os.path.join(
    self_directory, "endpoints.openapi.yaml"
)


def get_models_filename():
    return os.path.join(self_directory, "models.py")


def implementation_filename(operationId, extension=""):
    return os.path.join(
        self_directory,
        "views",
        "{}{}{}.py".format(
            operationId.name(),
            operationId.variant(),
            extension,
        ),
    )


def definition_filename(operationId):
    return implementation_filename(
        operationId, extension="definition"
    )


OpenAPI.from_file_path(openapi_filename)

with open(openapi_filename, "r") as file:
    openapi_raw = yaml.safe_load(file.read())
    openapi = RefInjector(openapi_raw["components"])(openapi_raw)


def get_raw_operation(operationId):
    for path, method in openapi_raw["paths"].items():
        for operation in method.values():
            if operationId == operation["operationId"]:
                return operation


def traverse_api(should_yield_keys_value):
    stack = [openapi]
    while True:
        next = stack.pop()
        if isinstance(next, dict):
            for key, value in next.items():
                if should_yield_keys_value(key):
                    yield value
                stack.append(value)
        elif isinstance(next, list):
            stack.extend(next)
        if len(stack) == 0:
            break


operations = {}
operation_paths = {}

for path, method in openapi["paths"].items():
    for operation in method.values():
        id = operation["operationId"]
        operations[id] = operation
        operation_paths[id] = path


def map_tree(mapper, schema, data):
    if not data:
        return data
    elif isinstance(data, dict):
        return {
            key: map_tree(mapper, schema["properties"][key], value)
            for key, value in data.items()
        }
    elif isinstance(data, list) or isinstance(data, set):
        return [
            map_tree(mapper, schema["items"], value) for value in data
        ]
    else:
        return mapper(data, schema)


def response_definitions(operations=operations, id=None):
    for operation in operations.values():
        for code, description in operation["responses"].items():
            operationId = OperationId(operation["operationId"])
            if id and operationId != id:
                continue
            yield ResponseDescription(
                code,
                operationId,
                description["description"],
                description["content"]["*"]["schema"],
            )


def get_request_body_arguments(operation):
    try:
        return operation["requestBody"]["content"]["*"]["schema"][
            "properties"
        ].keys()
    except KeyError:
        return []


def get_parameter_arguments(operation):
    try:
        return [
            parameter["name"] for parameter in operation["parameters"]
        ]
    except KeyError:
        return []
