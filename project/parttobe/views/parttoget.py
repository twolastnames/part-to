from datetime import timedelta
from parttobe import models


def handle(arguments):
    definitions = models.order_definitions(
        list(arguments.partTo.task_definitions)
    )
    return arguments.respond_200(
        {
            "workDuration": timedelta(
                seconds=sum(
                    [
                        definition.weight().seconds
                        for definition in definitions
                    ]
                )
            ),
            "clockDuration": definitions[0].chain_duration(),
            "name": arguments.partTo.name,
            "tasks": definitions,
        }
    )
