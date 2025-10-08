from django.db import transaction
from parttobe import models
import datetime
from rest_framework.response import Response


def ensure_list(value):
    return value if isinstance(value, list) else [value]


def check_duration(task):
    return task["duration"].seconds < 1


def check_task(task):
    missing = []
    for key in ["duration", "description"]:
        if key not in task:
            missing.append(key)
    return missing


def invert_depends(tasks):
    invertion = {}
    for name, task in traverse_tasks(tasks):
        if "depends" not in task:
            continue
        for depend in task["depends"]:
            invertion[depend] = name
    return invertion


@transaction.atomic
def save_job(tasks):
    part_to = models.PartTo.objects.create(name=tasks["part_to"]["name"])
    saved_tasks = {}
    for key, definition in tasks.items():
        if key == "part_to":
            continue
        saved_tasks[key] = models.TaskDefinition.objects.create(
            initial_duration=definition["duration"],
            part_to=part_to,
            description=definition["description"],
            engagement=(
                definition["engagement"]
                if "engagement" in definition and definition["engagement"] > 0
                else None
            ),
        )
        for ingredient in (
            ensure_list(definition["ingredients"])
            if "ingredients" in definition
            else []
        ):
            models.IngredientDefinition.objects.create(
                name=ingredient,
                task=saved_tasks[key],
            )
        for tool in ensure_list(definition["tools"]) if "tools" in definition else []:
            models.ToolDefinition.objects.create(
                name=tool,
                task=saved_tasks[key],
            )
    for key, definition in tasks.items():
        if key == "part_to":
            continue
        if "depends" not in definition:
            continue
        for dependency in ensure_list(definition["depends"]):
            models.Dependent.objects.create(
                dependency=saved_tasks[dependency], depended=saved_tasks[key]
            )
    for saveable in saved_tasks.values():
        saveable.save()
    return part_to.uuid

    dependeds = invert_depends(tasks)
    saved_tasks = {}
    stack = tasks["part_to"]["depends"][:]
    while len(stack) > 0:
        current = stack.pop()
        if current in saved_tasks:
            continue
        if current in dependeds and dependeds[current] not in saved_tasks:
            stack.insert(0, current)
            continue
        depended = saved_tasks[dependeds[current]] if current in dependeds else None
        task = tasks[current]
        if "depends" in task:
            stack.extend(task["depends"])
        saved_tasks[current] = models.TaskDefinition.objects.create(
            initial_duration=task["duration"],
            depended=depended,
            part_to=part_to,
            description=task["description"],
            engagement=(
                task["engagement"]
                if "engagement" in task and task["engagement"] > 0
                else None
            ),
        )
        for ingredient in (
            ensure_list(task["ingredients"]) if "ingredients" in task else []
        ):
            models.IngredientDefinition.objects.create(
                name=ingredient,
                task=saved_tasks[current],
            )
        for tool in ensure_list(task["tools"]) if "tools" in task else []:
            models.ToolDefinition.objects.create(
                name=tool,
                task=saved_tasks[current],
            )
    return part_to.uuid


class UnusedTaskFoundException(RuntimeError):
    def __init__(self, task_name):
        self.task_name = task_name
        super().__init__()

    def __str__(self):
        return 'Unused Task(s): "{}"'.format(self.task_name)


class TaskNotFoundException(RuntimeError):
    def __init__(self, task_name):
        self.task_name = task_name
        super().__init__()

    def __str__(self):
        return 'Missing Task(s): "{}"'.format(self.task_name)


class CyclicTaskDependencyException(RuntimeError):
    def __init__(self, dependency):
        self.dependency = dependency
        super().__init__()

    def __str__(self):
        return 'Cyclic dependency in "{}"'.format(self.dependency)


class MissingTaskKeyException(RuntimeError):
    def __init__(self, task_name, key_name):
        self.task_name = task_name
        self.key_name = key_name
        super().__init__()

    def __str__(self):
        return 'Missing "{}" key on: "{}"'.format(self.key_name, self.task_name)


class GeneralErrorException(RuntimeError):
    def __init__(self, task_name, key_name, error):
        self.task_name = task_name
        self.key_name = key_name
        self.error = error
        super().__init__()

    def __str__(self):
        return '"{}" {}: "{}"'.format(self.task_name, self.error, self.key_name)


def traverse_tasks(tasks):
    for key, task in tasks.items():
        if "depends" in task and key in task["depends"]:
            raise CyclicTaskDependencyException(key)
    seen_keys = set()
    if "part_to" not in tasks:
        raise TaskNotFoundException("part_to")
    seen_keys.add("part_to")
    part_to = tasks["part_to"]
    if "depends" not in part_to:
        raise MissingTaskKeyException("part_to", "depends")
    if "name" not in part_to:
        raise MissingTaskKeyException("part_to", "name")
    stack = part_to["depends"][:]
    while len(stack) > 0:
        current = stack.pop()
        seen_keys.add(current)
        if current not in tasks:
            raise TaskNotFoundException(current)
        if "depends" in tasks[current]:
            for stacked in stack:
                if "depends" not in tasks[stacked]:
                    continue
                if (
                    current in tasks[stacked]["depends"]
                    and stacked in tasks[current]["depends"]
                ):
                    raise CyclicTaskDependencyException(stacked)
        task = tasks[current]
        yield current, task
        if "depends" in task:
            for depend in task["depends"]:
                stack.append(depend)
    all_keys = set(tasks.keys())
    extra_keys = all_keys - seen_keys
    if extra_keys:
        raise UnusedTaskFoundException(",".join(extra_keys))


def verify_tasks(tasks):
    for name, task in traverse_tasks(tasks):
        missing = check_task(task)
        if len(missing) > 0:
            raise MissingTaskKeyException(name, ",".join(missing))
        zero = check_duration(task)
        if zero:
            raise GeneralErrorException(
                "duration", name, "must be greater than 1 second on"
            )


def request_to_dictionary(part_to, tasks):
    return {"part_to": part_to} | {task["name"]: task for task in tasks}


def validate(part_to=None, tasks=None):
    tasks = request_to_dictionary(part_to, tasks)
    try:
        verify_tasks(tasks)
    except RuntimeError as exception:
        return (
            {"messages": [str(exception)]},
            "400",
        )


def handle(argument):
    validation = validate(argument.part_to, argument.tasks)
    if validation:
        return Response(validation[0]["messages"], 400)
    together = {"part_to": argument.part_to} | {
        task["name"]: task for task in argument.tasks
    }
    id = save_job(together)
    return {
        "partTo": str(id),
        "message": "job insert successfull",
    }
