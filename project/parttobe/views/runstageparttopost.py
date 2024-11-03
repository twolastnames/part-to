from parttobe import models
from parttobe.views.helpers import handle_run_state


def handle(arguments):
    definitions = [
        definition
        for definition in partTo.task_definitions
        for partTo in arguments.partTos
    ]
    return arguments.respond_200(
        handle_run_state(
            models.RunState.Operation.STAGED,
            definitions,
            arguments.runState,
        )
    )
