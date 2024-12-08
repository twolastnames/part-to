import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
from freezegun import freeze_time
from datetime import timedelta
import json
import parttobe.models as models
import os
import toml
import copy
from parttobe.views.test_helpers import (
    SHARED_UUID,
    use_shared_uuid,
)
from parttobe.views.test_nondjango_helpers import (
    get_toml_recipe_as_json,
    toml_to_body,
)


class PartToPostTestClass(TestCase):
    def setUp(self):
        models.get_task_definitions.cache_clear()

    def test_missing_part_to(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = get_toml_recipe_as_json(
            file_directory + "/../mocks_partto/baked_beans.toml"
        )
        del data["part_to"]
        response = client.post(
            "/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            ["'part_to' is a required property"],
        )

    def test_missing_part_to_name(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = get_toml_recipe_as_json(
            file_directory + "/../mocks_partto/baked_beans.toml"
        )
        del data["part_to"]["name"]
        response = client.post(
            "/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), ["'name' is a required property"]
        )

    def test_missing_part_to_depends(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = get_toml_recipe_as_json(
            file_directory + "/../mocks_partto/baked_beans.toml"
        )
        del data["part_to"]["depends"]
        response = client.post(
            "/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            ["'depends' is a required property"],
        )

    def test_missing_duration(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = get_toml_recipe_as_json(
            file_directory + "/../mocks_partto/baked_beans.toml"
        )
        for task in data["tasks"]:
            if task["name"] != "simmer_beans":
                return
            del task["duration"]
        response = client.post(
            "/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"message": 'Missing "duration" key on: "Simmer Beans"'},
        )

    def test_missing_task(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = get_toml_recipe_as_json(
            file_directory + "/../mocks_partto/baked_beans.toml"
        )
        data["tasks"] = [
            task for task in data["tasks"] if task["name"] != "simmer_beans"
        ]
        response = client.post(
            "/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), ['Missing Task(s): "simmer_beans"']
        )

    def test_unused_task(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        data = get_toml_recipe_as_json(
            file_directory + "/../mocks_partto/baked_beans.toml"
        )
        data["tasks"].append(
            {
                "name": "Play Euchre",
                "duration": 25 * 60,
                "description": "take a break and play a game of euchre with your family darn it",
                "ingredients": [],
                "tools": [],
            }
        )
        response = client.post(
            "/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), ['Unused Task(s): "Play Euchre"']
        )

    def test_can_read_job_successfully(self):
        file_directory = os.path.dirname(__file__)
        client = Client()
        post_response = client.post(
            "/api/partto/",
            json.dumps(
                get_toml_recipe_as_json(
                    file_directory + "/../mocks_partto/baked_beans.toml"
                )
            ),
            content_type="*",
        )
        self.assertEqual(post_response.status_code, 200)
        body = json.loads(post_response.content)
        get_response = client.get("/api/partto/?partTo={}".format(body["partTo"]))
        self.assertEqual(get_response.status_code, 200)
        taskless = copy.deepcopy(get_response.data)
        del taskless["tasks"]
        self.assertEqual(
            taskless,
            {
                "workDuration": 926.0,
                "clockDuration": 9248.5,
                "name": "Baked Beans (Easy)",
            },
        )
        self.assertEqual(len(get_response.data["tasks"]), 14)
