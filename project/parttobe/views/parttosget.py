from parttobe import models


def handle(arguments):
    return {
        "partTos": list(models.PartTo.displayables()),
    }
