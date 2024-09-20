from parttobe import models


def handle(arguments):
    part_to = models.PartTo.objects.get(uuid=arguments.id)
    return arguments.respond_200(
        part_to.uuid,
        part_to.name,
        [task.uuid for task in part_to.task_definitions],
    )


def create200Body(uuid, name, tasks):
    return {
        "id": uuid,
        "name": name,
        "tasks": tasks,
    }
