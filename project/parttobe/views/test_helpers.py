from django.test import TestCase
from django.test import Client
from freezegun import freeze_time
from parttobe import models
from datetime import timedelta
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
    models.get_task_definitions.cache_clear()
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
        data = get_toml_recipe_as_json(file_directory + "/../mocks_partto" + loadable)
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


class ClientTester(TestCase):
    def setUp(self):
        self.ids = loadExamples()

    def __init__(self, input):
        super().__init__(input)
        self.client = Client()
        self.definitionIds = {}

    def changeState(self, state, description):
        response = self.client.post(
            "/api/run/{}".format(state),
            {
                "runState": self.runState,
                "definitions": [self.definitionIds[description]],
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.runState = response.data["runState"]
        response = self.client.get("/api/run/?runState={}".format(self.runState))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Cache-Control"], "public, max-age=31536000, immutable"
        )
        self.runStateData = response.data

    def assertImminentDescriptions(self, *descriptions):
        self.assertEqual(len(descriptions), len(self.runStateData["imminent"]))
        for imminent, description in zip(self.runStateData["imminent"], descriptions):
            self.definitionIds[description] = imminent["duty"]
            response = self.client.get("/api/task/?task={}".format(imminent["duty"]))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.headers["Cache-Control"], "public, max-age=31536000, immutable"
            )
            self.assertEqual(response.data["description"], description)

    def assertImminentTills(self, *tills):
        self.assertEqual(len(tills), len(self.runStateData["imminent"]))
        for imminent, till in zip(self.runStateData["imminent"], tills):
            self.assertEqual(timedelta(seconds=imminent["till"]), till)

    def assertStartedDescriptions(self, *descriptions):
        self.assertEqual(len(descriptions), len(self.runStateData["started"]))
        for started, description in zip(self.runStateData["started"], descriptions):
            response = self.client.get("/api/task/?task={}".format(started))
            self.definitionIds[description] = started
            self.assertEqual(
                response.headers["Cache-Control"], "public, max-age=31536000, immutable"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual
            self.assertEqual(response.data["description"], description)

    def startPartTos(self, *names):
        response = self.client.get("/api/parttos/")
        self.assertEqual(response.status_code, 200)
        self.partToDatas = [
            {
                "response": self.client.get("/api/partto/?partTo={}".format(key)),
                "key": key,
            }
            for key in response.data["partTos"]
        ]
        self.runState = None
        for data in self.partToDatas:
            if data["response"].data["name"] not in names:
                continue
            runStateAppendage = {"runState": self.runState} if self.runState else {}
            response = self.client.post(
                "/api/run/stage",
                {"partTos": [data["key"]]} | runStateAppendage,
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.runState = response.data["runState"]
        response = self.client.post(
            "/api/run/start",
            {
                "runState": self.runState,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.runState = response.data["runState"]
        response = self.client.get("/api/run/?runState={}".format(self.runState))
        self.assertEqual(
            response.headers["Cache-Control"], "public, max-age=31536000, immutable"
        )
        self.assertEqual(response.status_code, 200)
        self.runStateData = response.data
