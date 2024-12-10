from parttobe import models
from parttobe.views.helpers import handle_run_state


def handle(arguments):
    return arguments.respond_200(
        {
            "runState": models.next_work(
                models.append_states(
                    models.RunState.Operation.VOIDED,
                    arguments.definitions,
                    arguments.runState,
                )
            )
        }
    )
