import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import json


class TaskTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()

    def test_can_fetch_tasks_in_correct_order(self):
        client = Client()
        response1 = client.get(
            "/api/partto/?partTo={}".format(self.ids[2])
        )
        self.assertEqual(response1.status_code, 200)
        payload1 = response1.data
        self.assertEqual(payload1["name"], "Corn on the Cob")
        self.assertEqual(len(payload1["tasks"]), 5)

        response = client.get(
            "/api/task/?task={}".format(payload1["tasks"][0])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            "boil water in large pot", response.data["description"]
        )

        response = client.get(
            "/api/task/?task={}".format(payload1["tasks"][1])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            "wash the corn", response.data["description"]
        )

        response = client.get(
            "/api/task/?task={}".format(payload1["tasks"][2])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            "cut partially with kitchen shears to weaken cob middle to break in half",
            response.data["description"],
        )

        response = client.get(
            "/api/task/?task={}".format(payload1["tasks"][3])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            "put corn in and boil", response.data["description"]
        )

        response = client.get(
            "/api/task/?task={}".format(payload1["tasks"][4])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            "remove from heat", response.data["description"]
        )

    def test_200s_unknown_parameter(self):
        client = Client()
        response = client.get("/api/task/?task=1".format(self.ids[0]))
        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.data)
