import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import json


class RunStageTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()

    def test_will_fail_stage_input(self):
        client = Client()
        data = json.dumps({"partTos": [self.ids[1]]})
        client = Client()
        response = client.post(
            "/api/run/void", data, content_type="*"
        )
        self.assertEqual(response.status_code, 400)

    def test_can_start_run(self):
        client = Client()
        data = json.dumps({"partTos": [self.ids[3]]})
        response = client.post(
            "/api/run/stage", data, content_type="*"
        )
        runStateId = response.data["runState"]
        self.assertEqual(response.status_code, 200)
        response = client.get(
            "/api/partto/?partTo={}".format(self.ids[3])
        )
        self.assertEqual(response.status_code, 200)
        voidable = response.data["tasks"][2]
        data = json.dumps(
            {
                "definitions": [voidable],
                "runState": runStateId,
            }
        )
        response = client.post(
            "/api/run/void", data, content_type="*"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("runState" in response.data)
        runStateId = response.data["runState"]
        response = client.get(
            "/api/run/?runState={}".format(runStateId)
        )
        self.assertEqual(response.status_code, 200)
        runState = response.data["runState"]
        voided = response.data["voided"][0]
        response = client.get(
            "/api/run/?runState={}".format(runStateId)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["voided"], [voided])
        self.assertEqual(
            response.data["activePartTos"], [self.ids[3]]
        )
