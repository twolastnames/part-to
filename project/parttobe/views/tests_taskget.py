import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import json

import parttobe.models as m


class TaskTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()

    def test_can_fetch_tasks_in_correct_order(self):
        client = Client()
        response = client.get("/api/parttos/")
        self.assertEqual(response.status_code, 200)
        partTo = response.data["partTos"][2]
        response1 = client.get("/api/partto/?partTo={}".format(partTo))
        self.assertEqual(response1.status_code, 200)
        payload1 = response1.data
        self.assertEqual(payload1["name"], "Corn on the Cob")
        self.assertEqual(len(payload1["tasks"]), 5)

        response = client.get("/api/task/?task={}".format(payload1["tasks"][0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Cache-Control"], "public, max-age=31536000, immutable"
        )
        self.assertEqual("boil water in large pot", response.data["description"])
        self.assertEqual([], response.data["ingredients"])
        self.assertEqual(["large pot"], response.data["tools"])

        response = client.get("/api/task/?task={}".format(payload1["tasks"][1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual("wash the corn", response.data["description"])
        self.assertEqual(["cobbed corn"], response.data["ingredients"])
        self.assertEqual(partTo, response.data["partTo"])

        response = client.get("/api/task/?task={}".format(payload1["tasks"][2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            "cut partially with kitchen shears to weaken cob middle to break in half",
            response.data["description"],
        )

        response = client.get("/api/task/?task={}".format(payload1["tasks"][3]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual("put corn in and boil", response.data["description"])

        response = client.get("/api/task/?task={}".format(payload1["tasks"][4]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual("remove from heat", response.data["description"])

    def test_200s_unknown_parameter(self):
        client = Client()
        response = client.get("/api/parttos/")
        self.assertEqual(response.status_code, 200)
        response1 = client.get(
            "/api/partto/?partTo={}".format(response.data["partTos"][2])
        )
        self.assertEqual(response1.status_code, 200)
        payload1 = response1.data
        self.assertEqual(payload1["name"], "Corn on the Cob")
        self.assertEqual(len(payload1["tasks"]), 5)
        response = client.get(
            "/api/task/?task={}&unknown=5".format(payload1["tasks"][1])
        )
        self.assertEqual(response.status_code, 200)
