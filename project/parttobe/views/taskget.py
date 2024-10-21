from parttobe import models


def handle(arguments):
    return {
        "duration": arguments.task.duration,
        "description": arguments.task.description,
    }
