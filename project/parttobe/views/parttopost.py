from django.db import transaction
from parttobe import models
import datetime

# import duration_parser


def ensure_list(value):
    return value if isinstance(value, list) else [value]


def check_task(task):
    missing = []
    for key in ["duration", "description"]:
        if key not in task:
            missing.append(key)
    return missing


def traverse_tasks(tasks):
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
        task = tasks[current]
        yield current, task
        if "depends" in task:
            for depend in task["depends"]:
                stack.append(depend)
    all_keys = set(tasks.keys())
    extra_keys = all_keys - seen_keys
    if extra_keys:
        raise UnusedTaskFoundException(",".join(extra_keys))


def invert_depends(tasks):
    invertion = {}
    for name, task in traverse_tasks(tasks):
        if "depends" not in task:
            continue
        for depend in task["depends"]:
            invertion[depend] = name
    return invertion


@transaction.atomic
def save_job(tasks, dependeds):
    saved_tasks = {}
    part_to = models.PartTo.objects.create(name=tasks["part_to"]["name"])
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
            engagement=(task["engagement"] if "engagement" in task else None),
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


class MissingTaskKeyException(RuntimeError):
    def __init__(self, task_name, key_name):
        self.task_name = task_name
        self.key_name = key_name
        super().__init__()

    def __str__(self):
        return 'Missing "{}" key on: "{}"'.format(self.key_name, self.task_name)


def traverse_tasks(tasks):
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
        return argument.respond_400(validation[0]["messages"])
    together = {"part_to": argument.part_to} | {
        task["name"]: task for task in argument.tasks
    }
    id = save_job(together, invert_depends(together))
    return argument.respond_200(
        {
            "partTo": str(id),
            "message": "job insert successfull",
        }
    )
