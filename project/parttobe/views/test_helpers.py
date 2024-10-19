from django.test import TestCase
from django.test import Client
from freezegun import freeze_time
import json
import toml
import os
import urllib
from unittest import mock
import uuid
import re
from parttobe.views.test_nondjango_helpers import (
    get_toml_recipe_as_json,
)


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
        data = get_toml_recipe_as_json(
            file_directory + "/../job_examples" + loadable
        )
        response = client.post(
            "http://testserver/api/partto/",
            json.dumps(data),
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
            ids.append(response.data["partTo"])
    return ids
