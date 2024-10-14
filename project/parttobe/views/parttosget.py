from parttobe import models


def handle(arguments):
    return arguments.respond_200(
        {
            "partTos": list(models.PartTo.objects.all()),
        }
    )
