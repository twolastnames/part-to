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


def implementation_filename(operationId):
    return "{}/openapiviews/{}{}.py".format(
        self_directory,
        operationId.name(),
        operationId.variant(),
    )


OpenAPI.from_file_path(openapi_filename)

with open(openapi_filename, "r") as file:
    openapi_raw = yaml.safe_load(file.read())
    openapi = RefInjector(openapi_raw["components"])(openapi_raw)
