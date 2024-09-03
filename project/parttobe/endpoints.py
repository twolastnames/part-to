import os
import yaml
from openapi_core import OpenAPI
import functools


class OperationId:
    def __init__(self, value):
        self.value = value

    def name(self):
        return self.value.split(":")[0]

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


self_directory = os.path.dirname(os.path.abspath(__file__))
openapi_filename = self_directory + "/endpoints.openapi.yaml"


def implementation_filename(operationId, extension=""):
    return "{}/openapiviews/{}{}{}.py".format(
        self_directory,
        operationId.name(),
        operationId.variant(),
        extension,
    )


def definition_filename(operationId):
    return implementation_filename(
        operationId, extension="definition"
    )


OpenAPI.from_file_path(openapi_filename)

with open(openapi_filename, "r") as file:
    openapi_raw = yaml.safe_load(file.read())
    openapi = RefInjector(openapi_raw["components"])(openapi_raw)

operations = {}

for method in openapi["paths"].values():
    for operation in method.values():
        id = operation["operationId"]
        operations[id] = operation


def get_request_body_arguments(operation):
    try:
        return operation["requestBody"]["content"][
            "application/json"
        ]["schema"]["properties"].keys()
    except KeyError:
        return []


def get_parameter_arguments(operation):
    try:
        return [
            parameter["name"] for parameter in operation["parameters"]
        ]
    except KeyError:
        return []
