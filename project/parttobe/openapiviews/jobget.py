from parttobe import models


def handle(id=None):
    part_to = models.PartTo.objects.get(uuid=id)

    payload = {
        "id": part_to.uuid,
        "name": part_to.name,
        "tasks": [task.uuid for task in part_to.task_definitions],
    }
    return payload
