import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import json


class TaskDurationMetricTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()

    def test_can_get_first_estimated_duration(self):
        client = Client()
        response = client.get("/api/partto/?partTo={}".format(self.ids[2]))
        self.assertEqual(response.status_code, 200)
        task = response.data["tasks"][0]
        response = client.get("/api/metric/task?task={}".format(task))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["estimatedDuration"],
            60.0,
        )
        self.assertEqual(response.data["from"], [])
        self.assertEqual(
            response.data["initialEstimation"]["usedInCalculation"],
            True,
        )
