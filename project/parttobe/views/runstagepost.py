from parttobe import models
from parttobe.views.helpers import handle_run_state


def handle(arguments):
    return handle_run_state(
        models.RunState.Operation.STAGED,
        [
            definition
            for partTo in arguments.partTos
            for definition in partTo.task_definitions
        ],
        arguments.runState,
    )
