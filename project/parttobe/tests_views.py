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

SHARED_UUID = "12345678-1234-4321-1234-123456789021"


def use_shared_uuid(content):
    value_lengths = [8, 4, 4, 4, 12]
    expression = "-".join(
        list(map(lambda l: "[\da-fA-F]{{{count}}}".format(count=l), value_lengths))
    )
    text = content.decode("utf-8")
    substituted = re.sub(expression, SHARED_UUID, text)
    return substituted


class HelloWorldTestCase(TestCase):
    def test_hello_world(self):
        client = Client()
        response = client.get("/api/hello-world/", format="json")
        self.assertEqual(json.loads(response.content), {"message": "Hello, world!"})


def toml_to_body(toml):
    body = {"part_to": toml["part_to"]}
    tasks = {k: v for (k, v) in toml.items() if k != "part_to"}
    body["tasks"] = [v1 | {"name": k1} for (k1, v1) in tasks.items()]
    return body


def job_body_from_key(key):
    file_directory = os.path.dirname(__file__)
    raw = toml.load(file_directory + "/job_examples/{}.toml".format(key))
    return json.dumps(toml_to_body(raw))


@mock.patch(
    "uuid.uuid4", mock.MagicMock(return_value="12345678-1234-4321-1234-123456789021")
)
def loadExamples():
    file_directory = os.path.dirname(__file__)
    client = Client()
    loadables = [
        "/baked_beans.toml",
        "/bavarian_pot_roast.toml",
        "/corn_on_the_cob.toml",
        "/frozen_green_beans.toml",
    ]
    for loadable in loadables:
        toml_structure = toml_to_body(
            toml.load(file_directory + "/job_examples" + loadable)
        )
        data = json.dumps(toml_structure)
        response = client.post(
            "http://testserver/api/job/", data, content_type="application/json"
        )
        if response.status_code != 200:
            raise Exception(
                "{} did not work with status {} with message: {}".format(
                    loadable, response.status_code, response.content
                )
            )


class UploadJobCase(TestCase):
    def test_missing_part_to(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = toml.load(file_directory + "/job_examples/baked_beans.toml")
        del data["part_to"]
        response = client.post(
            "/api/job/", json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"message": 'Missing Task(s): "part_to"'}
        )

    def test_missing_part_to_name(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = toml.load(file_directory + "/job_examples/baked_beans.toml")
        del data["part_to"]["name"]
        response = client.post(
            "/api/job/", json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"message": 'Missing "name" key on: "part_to"'},
        )

    def test_missing_part_to_depends(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = toml.load(file_directory + "/job_examples/baked_beans.toml")
        del data["part_to"]["depends"]
        response = client.post(
            "/api/job/", json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"message": 'Missing "depends" key on: "part_to"'},
        )

    def test_missing_duration(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = toml.load(file_directory + "/job_examples/baked_beans.toml")
        del data["simmer_beans"]["duration"]
        response = client.post(
            "/api/job/", json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"message": 'Missing "duration" key on: "simmer_beans"'},
        )

    def test_missing_task(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = toml.load(file_directory + "/job_examples/baked_beans.toml")
        del data["simmer_beans"]
        response = client.post(
            "/api/job/", json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"message": 'Missing Task(s): "simmer_beans"'}
        )

    def test_unused_task(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = toml.load(file_directory + "/job_examples/baked_beans.toml")
        data["play_euchre"] = {
            "duration": "15 minutes",
            "description": "take a break and play a game of euchre with your family darn it",
        }
        response = client.post(
            "/api/job/", json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"message": 'Unused Task(s): "play_euchre"'}
        )

    def test_can_read_job_successfully(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        post_response = client.post(
            "/api/job/",
            job_body_from_key("baked_beans"),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 200)
        body = json.loads(post_response.content)
        get_response = client.get("/api/job/?id={}".format(body["id"]))
        self.assertEqual(get_response.status_code, 200)
        loaded_content = json.loads(get_response.content)
        self.assertEqual(loaded_content["id"], body["id"])
        self.assertEqual(
            json.loads(use_shared_uuid(get_response.content)),
            {
                "id": SHARED_UUID,
                "name": "Baked Beans (Easy)",
                "tasks": [SHARED_UUID for task in range(14)],
            },
        )


class ListToolsTestClass(TestCase):
    def setUp(self):
        loadExamples()

    def test_can_get_ingredients(self):
        client = Client()
        params = urllib.parse.urlencode(
            [
                ("name[]", "Bavarian Pot Roast"),
                ("name[]", "Corn on the Cob"),
            ]
        )
        response = client.get("/api/tools/?" + params, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content), ["dutch oven", "kitchen shears", "large pot"]
        )

    def test_unknown_name(self):
        client = Client()
        params = urllib.parse.urlencode(
            [
                ("name[]", "Not a name"),
                ("name[]", "Corn on the Cob"),
            ]
        )
        response = client.get("/api/tools/?" + params, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"message": 'Unknown Job Name(s): "Not a name"'},
        )

    def test_2_unknown_names(self):
        client = Client()
        params = urllib.parse.urlencode(
            [
                ("name[]", "Not a name"),
                ("name[]", "Corn on the Cob"),
                ("name[]", "Not a name2"),
            ]
        )
        response = client.get("/api/tools/?" + params, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"message": 'Unknown Job Name(s): "Not a name", "Not a name2"'},
        )


class ListIngredientsTestClass(TestCase):
    def setUp(self):
        loadExamples()

    def test_can_get_ingredients(self):
        client = Client()
        params = urllib.parse.urlencode(
            [("name[]", "Bavarian Pot Roast"), ("name[]", "Corn on the Cob")]
        )
        response = client.get("/api/ingredients/?" + params, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            [
                "bay leaf, 1",
                "beef chuck roast, boneless, 1 roast, about 3 lbs",
                "beer or beef broth, 3/4 cup",
                "canola oil, 2 tbs",
                "chopped onion, 1/2",
                "cinnamon, ground, 1 tsp",
                "cobbed corn",
                "ground ginger, 1/2 tsp",
                "pepper, 1/2 tsp",
                "salt, 1 tsp",
                "sugar, 2 tbs",
                "tomato sauce, 8 oz",
                "water, 1 1/4 cup",
                "white vinegar, 1 tbs",
            ],
        )

    def test_unknown_name(self):
        client = Client()
        params = urllib.parse.urlencode(
            [
                ("name[]", "Not a name"),
                ("name[]", "Corn on the Cob"),
            ]
        )
        response = client.get("/api/ingredients/?" + params, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"message": 'Unknown Job Name(s): "Not a name"'},
        )

    def test_2_unknown_names(self):
        client = Client()
        params = urllib.parse.urlencode(
            [
                ("name[]", "Not a name"),
                ("name[]", "Corn on the Cob"),
                ("name[]", "Not a name2"),
            ]
        )
        response = client.get("/api/ingredients/?" + params, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"message": 'Unknown Job Name(s): "Not a name", "Not a name2"'},
        )


TEST_UUIDS = ["uuid_{}".format(i) for i in range(10000)]


@mock.patch(
    "uuid.uuid4", mock.MagicMock(return_value="12345678-1234-4321-1234-123456789021")
)
class JobTestClass(TestCase):
    def setUp(self):
        loadExamples()

    def test_get_simple_job_set(self):
        client = Client()
        run_response = client.post(
            "/api/run/",
            data=json.dumps({"jobs": ["Frozen Green Beans"]}),
            content_type="application/json",
        )

    @freeze_time("2024-03-21 01:23:45")
    def test_get_simple_job_set(self):
        client = Client()
        run_response = client.post(
            "/api/run/",
            data=json.dumps({"jobs": ["Frozen Green Beans"]}),
            content_type="application/json",
        )
        first_duty = {
            "id": "12345678-1234-4321-1234-123456789021",
            "description": "boil water in large pot",
            "duration": 540000,
        }
        self.assertEqual(run_response.status_code, 200)
        content = json.loads(run_response.content)
        self.assertEqual(
            json.loads(use_shared_uuid(run_response.content)),
            {
                "id": "12345678-1234-4321-1234-123456789021",
                "report": "2024-03-21T01:23:45",
                "complete": "2024-03-21T01:28:19.800000",
                "duties": ["12345678-1234-4321-1234-123456789021"],
                "tasks": [],
            },
        )
        job_id = json.loads(run_response.content)["duties"][0]
        params = urllib.parse.urlencode(
            [
                ("id", job_id),
            ]
        )
        return
        job_response = client.get("/api/job/?" + params, format=json)
        self.assertEqual(job_response.status_code, 200)
        self.assertEqual(
            json.loads(use_shared_uuid(job_response.content)),
            {
                "description": "boil water in large pot",
                "duration": 540000,
            },
        )

    def test_get_job_set(self):
        client = Client()
        response = client.post(
            "/api/job_run",
            {
                "jobs": ["Baked Beans (Easy)", "Corn on the Cob"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "complete": "2024-03-29 15:29:10.418159",
                "tasks": ["taskId2"],
                "duties": ["dutyId1", "dutyId2"],
            },
        )

    def test_get_job_report(self):
        client = Client()
        response = client.get("/api/job/someId", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "complete": "2024-03-29 15:29:10.418159",
                "tasks": ["taskId2"],
                "duties": ["dutyId1", "dutyId2", "dutyId3"],
            },
        )


class TaskTestClass(TestCase):
    def test_get_running_task(self):
        client = Client()
        response = client.get("/api/task/someID", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "description": "Hello, world!",
                "status": "running",
                "duration": 77700,
            },
        )

    def test_get_waiting_task(self):
        client = Client()
        response = client.get("/api/task/someID", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "description": "Hello, world!",
                "status": "waiting",
                "duration": 77700,
            },
        )

    def test_patch_complete_task(self):
        client = Client()
        response = client.patch(
            "/api/task/taskId1", json.dumps({"status": "complete"}), format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "complete": "2024-03-29 15:29:10.418159",
                "tasks": ["taskId2"],
                "duties": ["dutyId1", "dutyId2"],
            },
        )

    def test_patch_complete_task_new_duty(self):
        client = Client()
        response = client.patch(
            "/api/task/taskId3", json.dumps({"status": "complete"}), format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "complete": "2024-03-29 15:29:10.418159",
                "tasks": ["taskId2"],
                "duties": ["dutyId1", "dutyId2", "dutyId3"],
            },
        )


class DutyTestClass(TestCase):
    def test_get_duty(self):
        client = Client()
        response = client.get("/api/duty/someId", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "description": "Do something cool",
                "duration": 55700,
            },
        )

    def test_patch_complete_duty(self):
        client = Client()
        response = client.patch(
            "/api/duty/duty1",
            json.dumps(
                {
                    "status": "complete",
                    "duration": 888880,
                }
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "complete": "2024-03-29 15:29:10.418159",
                "tasks": ["taskId2"],
                "duties": ["dutyId2"],
            },
        )
