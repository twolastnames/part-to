from parttobe import models


def handle(arguments):
    return arguments.respond_200(
        {
            "name": arguments.id.name,
            "tasks": arguments.id.task_definitions,
        }
    )
    # return arguments.respond_200(
    #    arguments.id.name,
    #    arguments.id.task_definitions
    #    #[task.uuid for task in arguments.id.task_definitions],
    # )


def create200Body(name, tasks):
    raise RuntimeError()
    # return {
    #    "name": name,
    #    "tasks": tasks,
    # }
