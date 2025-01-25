from parttobe import models
from parttobe.views.helpers import handle_run_state


def handle(arguments):
    runState = None
    if arguments.definitions:
        runState = models.append_states(
            models.RunState.Operation.STARTED,
            arguments.definitions,
            arguments.runState,
        )
    else:
        runState = arguments.runState
    return {"runState": models.next_work(runState)}
