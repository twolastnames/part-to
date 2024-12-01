import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import json


class RunStageTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()

    def test_can_start_run(self):
        client = Client()
        data = json.dumps({"partTos": [self.ids[2]]})
        client = Client()
        response = client.post("/api/run/stage", data, content_type="*")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("runState" in response.data)
        runStateId = response.data["runState"]
        state_response = client.get("/api/run/?runState={}".format(runStateId))
        self.assertEqual(state_response.status_code, 200)
        runState = state_response.data["runState"]
        startable = state_response.data["staged"][0]
        response = client.post(
            "/api/run/start",
            json.dumps(
                {
                    "runState": runState,
                }
            ),
            content_type="*",
        )
        self.assertEqual(response.status_code, 200)
        runStateId = response.data["runState"]
        response = client.get("/api/run/?runState={}".format(runStateId))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["started"], [startable])
        self.assertEqual(response.data["activePartTos"], [self.ids[2]])
