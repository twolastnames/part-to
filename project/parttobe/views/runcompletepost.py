from parttobe import models
from parttobe.views.helpers import handle_run_state


def handle(arguments):
    unstarted = []
    for definition in arguments.definitions:
        for state in arguments.runState.task_states():
            if state.task != definition:
                continue
            if state.operation != models.RunState.Operation.STARTED:
                unstarted.append(
                    "task {} is not in a started state".format(
                        definition.uuid
                    )
                )
    if len(unstarted) > 0:
        return arguments.respond_400(unstarted)

    return arguments.respond_200(
        handle_run_state(
            models.RunState.Operation.COMPLETED,
            [definition for definition in arguments.definitions],
            arguments.runState,
        )
    )
