def handle(arguments):
    return arguments.respond_200(
        {
            "name": arguments.partTo.name,
            "tasks": arguments.partTo.task_definitions,
        }
    )
