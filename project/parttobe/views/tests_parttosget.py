import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import json
import os
from parttobe.views.test_nondjango_helpers import (
    get_toml_recipe_as_json,
    toml_to_body,
)
import toml


class PartTosTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()

    def test_can_fetch_parttos(self):
        client = Client()
        response = client.get("/api/parttos/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["partTos"]), 4)

    def test_will_return_in_alphatic_order(self):
        client = Client()
        file_directory = os.path.dirname(__file__)
        data = get_toml_recipe_as_json(
            file_directory + "/../mocks_partto/brats_raw.toml"
        )
        response = client.post(
            "http://testserver/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        response = client.get("/api/parttos/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["partTos"]), 5)
        partTos = response.data["partTos"]
        response = client.get("/api/partto/?partTo={}".format(partTos[0]))
        self.assertEqual("Baked Beans (Easy)", response.data["name"])
        response = client.get("/api/partto/?partTo={}".format(partTos[1]))
        self.assertEqual("Bavarian Pot Roast", response.data["name"])
        response = client.get("/api/partto/?partTo={}".format(partTos[2]))
        self.assertEqual("Brats (raw)", response.data["name"])
        response = client.get("/api/partto/?partTo={}".format(partTos[3]))
        self.assertEqual("Corn on the Cob", response.data["name"])
        response = client.get("/api/partto/?partTo={}".format(partTos[4]))
        self.assertEqual("Frozen Green Beans", response.data["name"])

    def test_will_use_the_newer_recipe_with_same_name(self):
        client = Client()
        response = client.get("/api/parttos/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["partTos"]), 4)
        response = client.get(
            "/api/partto/?partTo={}".format(response.data["partTos"][0])
        )
        self.assertEqual("Baked Beans (Easy)", response.data["name"])
        file_directory = os.path.dirname(__file__)
        recipe = toml.load(file_directory + "/../mocks_partto/baked_beans.toml")
        recipe["let_cool"]["description"] = "be confused from this testing"
        data = toml_to_body(recipe)
        response = client.post(
            "http://testserver/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        response = client.get("/api/parttos/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["partTos"]), 4)
        response = client.get(
            "/api/partto/?partTo={}".format(response.data["partTos"][0])
        )
        self.assertEqual("Baked Beans (Easy)", response.data["name"])
        descriptions = []
        for task_id in response.data["tasks"]:
            response = client.get("/api/task/?task={}".format(task_id))
            descriptions.append(response.data["description"])
        self.assertIn("be confused from this testing", descriptions)

    def test_200s_unknown_parameter(self):
        client = Client()
        response = client.get("/api/parttos/?unknownOne=1".format(self.ids[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["partTos"]), 4)
