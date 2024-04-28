from django.test import TestCase
from django.test import Client
import json
import toml
import os
import urllib
from unittest import mock


class HelloWorldTestCase(TestCase):
    def test_hello_world(self):
        client = Client()
        response = client.get("/api/hello-world/", format="json")
        self.assertEqual(json.loads(response.content), {"message": "Hello, world!"})


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
        data = json.dumps(toml.load(file_directory + "/job_examples" + loadable))
        response = client.post("/api/job/", data, content_type="application/json")
        if response.status_code != 200:
            content = json.loads(response.content)
            raise Exception(
                "{} did not work with status {} with message: {}".format(
                    loadable, response.status_code, content["message"]
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
        self.assertEqual(json.loads(response.content), ["kitchen shears", "large pot"])

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
                "beer or beef broth, 3/4 cup",
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


class JobTestClass(TestCase):
    def setUp(self):
        loadExamples()

    @mock.patch(
        "uuid.uuid4",
        mock.MagicMock(return_value="12345678-1234-4321-1234-123456789021"),
    )
    @mock.patch("time.time", mock.MagicMock(return_value=12345))
    def test_get_simple_job_set(self):
        client = Client()
        response = client.post(
            "/api/run",
            {
                "jobs": ["Frozen Green Beans"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "12345678-1234-4321-1234-123456789021",
                "report": "2024-03-29 15:29:10.418159",
                "complete": "2024-03-29 15:29:10.418159",
                "duties": [
                    {
                        "description": "boil water in large pot",
                        "duration": 540000,
                    }
                ],
            },
        )

    def test_get_job_set(self):
        client = Client()
        response = client.post(
            "/api/job_run",
            {
                jobs: ["Baked Beans (Easy)", "Corn on the Cob"],
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
                "task": "taskId2",
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
                "task": "taskId2",
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
                "projectedSeconds": 77.7,
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
                "projectedSeconds": 77.7,
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
                "task": "taskId2",
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
                "task": "taskId4",
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
                "projectedSeconds": 55.7,
            },
        )

    def test_patch_complete_duty(self):
        client = Client()
        response = client.patch(
            "/api/duty/duty1",
            json.dumps(
                {
                    "status": "complete",
                    "duration": 888.88,
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
                "task": "taskId1",
                "duties": ["dutyId2"],
            },
        )
