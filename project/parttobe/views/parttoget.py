from datetime import timedelta
from parttobe import models
from parttobe.timeline import Timeline


def handle(arguments):
    definitions = models.order_definitions(list(arguments.partTo.task_definitions))
    *_, last = Timeline(definitions)
    return {
        "workDuration": timedelta(
            seconds=sum([definition.weight().seconds for definition in definitions])
        ),
        "clockDuration": last.till + last.id.duration,
        "name": arguments.partTo.name,
        "tasks": definitions,
    }
