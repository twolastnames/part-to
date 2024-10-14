from django.test import TestCase
from django.test import Client
from freezegun import freeze_time
from pytimeparse.timeparse import timeparse
import json
import toml
import os
import urllib
from unittest import mock
import uuid
import re


SHARED_UUID = "12345678-1234-4321-1234-123456789021"


def use_shared_uuid(content):
    value_lengths = [8, 4, 4, 4, 12]
    expression = "-".join(
        list(
            map(
                lambda l: "[\da-fA-F]{{{count}}}".format(count=l),
                value_lengths,
            )
        )
    )
    text = content.decode("utf-8")
    substituted = re.sub(expression, SHARED_UUID, text)
    return substituted


def map_definition(key, value):
    if "duration" in value:
        value["duration"] = timeparse(value["duration"])
    return value


def toml_to_body(toml):
    body = {"part_to": toml["part_to"]}
    tasks = {k: map_definition(k, v) for (k, v) in toml.items() if k != "part_to"}
    body["tasks"] = [v1 | {"name": k1} for (k1, v1) in tasks.items()]
    return body


def loadExamples():
    file_directory = os.path.dirname(__file__)
    client = Client()
    loadables = [
        "/baked_beans.toml",
        "/bavarian_pot_roast.toml",
        "/corn_on_the_cob.toml",
        "/frozen_green_beans.toml",
    ]
    ids = []
    for loadable in loadables:
        toml_structure = toml_to_body(
            toml.load(file_directory + "/../job_examples" + loadable)
        )
        data = json.dumps(toml_structure)
        response = client.post(
            "http://testserver/api/partto/",
            data,
            content_type="*",
        )
        if response.status_code != 200:
            raise Exception(
                "{} did not work with status {} with message: {}".format(
                    loadable,
                    response.status_code,
                    response.content,
                )
            )
        else:
            ids.append(json.loads(response.data)["partTo"])
    return ids
