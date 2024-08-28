from parttobe import models


def validate(id=None):
    """
    openapi has already been validated against
    this would be for application specific errors
    return an list of string errors ['error 1', 'error 2']
    """
    pass


def handle(id=None):
    print("id", id)
    part_to = models.PartTo.objects.get(uuid=id)

    payload = {
        "id": part_to.uuid,
        "name": part_to.name,
        "tasks": [task.uuid for task in part_to.task_definitions],
    }
    return payload
