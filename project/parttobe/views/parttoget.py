from datetime import timedelta


def handle(arguments):
    definitions = list(arguments.partTo.task_definitions)
    definitions.sort()
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
