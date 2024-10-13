from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import (
    IntegrityError,
    transaction,
)
from . import models
from pytimeparse.timeparse import timeparse
import datetime
import time
import json
import os

ROOT_TASK_NAME = "part_to"


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, world!"})


# this isn't connected, but here for when it is implemented with openapi
def job_get(request):
    id = request.args.get("id")
    definition = TaskDefinition.objects.get(uuid=id)
    return Response(json.dumps(definition))


def get_id_list(definitions):
    return list(
        map(
            lambda definition: definition.uuid,
            definitions,
        )
    )


def get_run_state(run):
    running_definitions = list(run.running_definitions())
    running_duties = get_id_list(run.running_duties())
    running_tasks = get_id_list(run.running_tasks())
    next_duty = datetime.datetime.now() + run.until_next_duty()
    current = sorted(list(running_definitions))
    if len(current) > 0:
        complete = (
            datetime.datetime.now() + current[0].chain_duration()
        )
    else:
        complete = None
    return {
        "id": run.uuid,
        "report": next_duty,
        "complete": complete,
        "duties": running_duties,
        "tasks": running_tasks,
    }


def run_post(request):
    part_tos = models.PartTo.objects.filter(
        name__in=request.data["jobs"]
    )
    run = models.start_run(part_tos)
    duties = []
    try:
        task = next(run)
        duties.append(
            {
                "id": task.uuid,
                "description": task.definition.description,
                "duration": int(
                    task.definition.duration.total_seconds() * 1000
                ),
            }
        )
    except StopIteration:
        pass
    running_definitions = run.running_definitions()
    next_duty = datetime.datetime.now() + run.until_next_duty()
    complete = (
        datetime.datetime.now() + task.definition.chain_duration()
    )
    return Response(get_run_state(run))


@api_view(["GET", "POST"])
def run(request):
    if request.method == "GET":
        raise NotImplementedError()
    return run_post(request)


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
            filter(
                lambda a: a not in part_to_checkers,
                part_tos_given,
            ),
        )
    )
    if len(missing_part_tos) > 0:
        return Response(
            {
                "message": "Unknown Job Name(s): {}".format(
                    missing_part_tos
                )
            },
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
