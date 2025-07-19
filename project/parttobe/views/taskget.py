from parttobe import models


def handle(arguments):
    return {
        "duration": arguments.task.duration,
        "description": arguments.task.description,
        "partTo": arguments.task.part_to,
        "ingredients": [
            ingredients.name
            for ingredients in models.IngredientDefinition.objects.filter(
                task=arguments.task
            )
        ],
        "tools": [
            tool.name
            for tool in models.ToolDefinition.objects.filter(task=arguments.task)
        ],
    }
