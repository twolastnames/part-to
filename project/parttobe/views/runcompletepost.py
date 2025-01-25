from parttobe import models
from parttobe.views.helpers import handle_run_state
from rest_framework.response import Response


def handle(arguments):
    unstarted = []
    starteds = set(
        [
            state.task
            for state in arguments.runState.task_states()
            if state.operation == models.RunState.Operation.STARTED
        ]
    )
    for definition in arguments.definitions:
        if definition in starteds:
            continue
        unstarted.append("task {} is not in a started state".format(definition.uuid))
    if len(unstarted) > 0:
        return Response(unstarted, 400)

    return {
        "runState": models.next_work(
            models.append_states(
                models.RunState.Operation.COMPLETED,
                arguments.definitions,
                arguments.runState,
            )
        )
    }
