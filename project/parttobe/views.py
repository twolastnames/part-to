from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError, transaction
from . import models
import duration_parser
import datetime

ROOT_TASK_NAME = 'part_to'

@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, world!"})


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
            stack.append(current)
            continue
        depended = saved_tasks[dependeds[current]] if current in dependeds else None
        task = tasks[current]
        if "depends" in task:
            stack.extend(task["depends"])
        saved_tasks[current] = models.TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(
                seconds=duration_parser.parse(task["duration"])
            ),
            depended=depended,
            part_to=part_to,
            description=task["description"],
            engagement=task["engagement"] if "engagement" in task else None,
        )
        for ingredient in task["ingredients"] if "ingredients" in task else []:
            models.IngredientDefinition.objects.create(
                name=ingredient, task=saved_tasks[current]
            )
        for tool in task["tools"] if "tools" in task else []:
            models.ToolDefinition.objects.create(name=tool, task=saved_tasks[current])
    for root in tasks["part_to"]["depends"]:
        models.PartToTaskDefinition.objects.create(
            part_to=part_to,
            depend=saved_tasks[root],
        )


def invert_depends(tasks):
    invertion = {}
    for name, task in traverse_tasks(tasks):
        if "depends" not in task:
            continue
        for depend in task["depends"]:
            invertion[depend] = name
    return invertion


def check_task(task):
    missing = []
    for key in ["duration", "description"]:
        if key not in task:
            missing.append(key)
    return missing


class UnusedTaskFoundException(Exception):
    def __init__(self, task_name):
        self.task_name = task_name
        super().__init__()

    def __str__(self):
        return 'Unused Task(s): "{}"'.format(self.task_name)


class TaskNotFoundException(Exception):
    def __init__(self, task_name):
        self.task_name = task_name
        super().__init__()

    def __str__(self):
        return 'Missing Task(s): "{}"'.format(self.task_name)


class MissingTaskKeyException(Exception):
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
    return


def job_post(request):
    tasks = request.data
    try:
        verify_tasks(tasks)
    except TaskNotFoundException as exception:
        return Response({"message": str(exception)}, 400)
    except MissingTaskKeyException as exception:
        return Response({"message": str(exception)}, 400)
    except UnusedTaskFoundException as exception:
        return Response({"message": str(exception)}, 400)
    except Exception as exception:
        return Response({"message": str(exception)}, 500)
    save_job(tasks, invert_depends(tasks))
    return Response({"message": "job insert successfull"})


def job_get(request):
    return Response(status=404)


@api_view(["GET", "POST"])
def job(request):
    if request.method == "GET":
        return job_get(request)
    return job_post(request)


def get_needs(request, need):
    collection = []
    part_tos_given = request.query_params.getlist("name[]")
    part_tos = models.PartTo.objects.filter(name__in=part_tos_given)
    tasks = models.TaskDefinition.objects.filter(part_to__in=part_tos)
    needed = need.objects.filter(task__in=tasks)
    part_to_checkers = list(map(lambda a: a.name, part_tos))
    missing_part_tos = ", ".join(
        map(
            lambda a: '"{}"'.format(a),
            filter(lambda a: a not in part_to_checkers, part_tos_given),
        )
    )
    if len(missing_part_tos) > 0:
        return Response(
            {"message": "Unknown Job Name(s): {}".format(missing_part_tos)},
            400,
        )
    payload = list(map(lambda a: a.name, needed))
    payload.sort()
    return Response(payload)


@api_view(["GET"])
def ingredients(request):
    return get_needs(request, models.IngredientDefinition)


@api_view(["GET"])
def tools(request):
    return get_needs(request, models.ToolDefinition)
