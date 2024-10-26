from parttobe import models
from parttobe.views.helpers import handle_run_state


def handle(arguments):
    return arguments.respond_200(
        handle_run_state(
            models.RunState.Operation.STAGED,
            arguments.definitions,
            arguments.runState,
        )
    )
