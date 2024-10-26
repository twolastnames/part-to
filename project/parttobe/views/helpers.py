import importlib
import sys
from parttobe import endpoints
from rest_framework.response import Response
from collections import namedtuple
from uuid import uuid4
from parttobe import models

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

    def responder(*args, **kargs):
        body = creator(*args, **kargs)
        return {"body": body, "status": status}

    return responder


class ViewResponse:
    def __init__(self, body_generator, description):
        pass

    def status(self):
        return self.status


def get_response_definition(description):
    body_constructor = get_body_constructor(description)
    return ViewResponse(body_constructor, description)


def handle_run_state(operation, definitions, runState):
    args = (operation, definitions)
    id = None
    if runState:
        new_state = runState.append_states(operation, definitions)
    else:
        new_state = models.append_states(operation, definitions)
    return {"runState": new_state}
