import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import json


class RunCompleteTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()

    def test_will_400_unstarted_tasks(self):
        client = Client()
        data = json.dumps({"partTos": [self.ids[2]]})
        response = client.post("/api/run/stage", data, content_type="*")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("runState" in response.data)
        runStateId = response.data["runState"]
        response = client.get("/api/partto/?partTo={}".format(self.ids[3]))
        self.assertEqual(response.status_code, 200)
        completable = response.data["tasks"][0]
        complete_body = json.dumps(
            {
                "runState": runStateId,
                "definitions": [completable],
            }
        )
        response = client.post("/api/run/complete", complete_body, content_type="*")
        self.assertEqual(response.status_code, 400)

    def test_can_start_run(self):
        client = Client()
        data = json.dumps({"partTos": [self.ids[3]]})
        response = client.post("/api/run/stage", data, content_type="*")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("runState" in response.data)
        runStateId = response.data["runState"]
        state_response = client.get("/api/run/?runState={}".format(runStateId))
        self.assertEqual(response.status_code, 200)

        data = json.dumps(
            {
                "runState": runStateId,
            }
        )
        response = client.post("/api/run/start", data, content_type="*")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("runState" in response.data)
        response = client.get("/api/run/?runState={}".format(response.data["runState"]))
        self.assertTrue("started" in response.data)
        runStateId = response.data["runState"]
        self.assertEqual(response.status_code, 200)
        completable = response.data["started"][0]
        task = response.data["duties"][0]
        self.assertEqual(task, completable)
        complete_body = json.dumps(
            {
                "runState": runStateId,
                "definitions": [completable],
            }
        )
        response = client.post("/api/run/complete", complete_body, content_type="*")
        self.assertEqual(response.status_code, 200)
        response = client.get("/api/run/?runState={}".format(response.data["runState"]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("startTimes" in response.data)
        self.assertEqual(response.data["completed"], [completable])
