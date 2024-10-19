import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
from freezegun import freeze_time
from datetime import timedelta
import json


class PartToTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()

    def test_can_fetch_partto(self):
        client = Client()
        response = client.get(
            "/api/partto/?partTo={}".format(self.ids[0])
        )
        self.assertEqual(response.status_code, 200)
        # payload = json.loads(response.data)
        payload = response.data
        self.assertEqual(payload["name"], "Baked Beans (Easy)")
        self.assertEqual(
            payload["clockDuration"], timedelta(seconds=9085)
        )
        self.assertEqual(
            payload["workDuration"], timedelta(seconds=1966)
        )
        self.assertEqual(len(payload["tasks"]), 14)

    def test_400s_missing_parameter(self):
        client = Client()
        response = client.get("/api/partto/?unusedOne=1")
        self.assertEqual(response.status_code, 400)

    def test_200s_unknown_parameter(self):
        client = Client()
        response = client.get(
            "/api/partto/?unknownOne=1&partTo={}".format(self.ids[0])
        )
        self.assertEqual(response.status_code, 200)
