import importlib
import sys
from parttobe import endpoints
from rest_framework.response import Response
from collections import namedtuple
from uuid import uuid4

ResponseDescription = namedtuple(
    "ResponseDescription", ["status", "id", "description", "schema"]
)


class CodeNotMatchingConfig(RuntimeError):
    pass


def get_body_constructor(id_value, status):
    id = endpoints.OperationId(id_value)
    filename = "./parttobe/views/{}.py".format(id.slug())
    definition = "create{}Body".format(status)
    spec = importlib.util.spec_from_file_location(
        definition, filename
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[definition] = module
    loaded = spec.loader.exec_module(module)
    try:
        creator = getattr(module, definition)
    except (KeyError, AttributeError):
        message = "method {} needs to be defined in {}".format(
            definition, filename
        )
        # raise CodeNotMatchingConfig(message)

    def responder(*args, **kargs):
        body = creator(*args, **kargs)
        return {"body": body, "status": status}
        # return Response(body, status)

    return responder


class ViewResponse:
    def __init__(self, body_generator, description):
        pass

    def status(self):
        return self.status


def get_response_definition(description):
    body_constructor = get_body_constructor(description)
    return ViewResponse(body_constructor, description)
