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

    def test_can_start_first_tasks(self):
        client = Client()
        response = client.get("/api/parttos/")
        self.assertEqual(response.status_code, 200)
        partTos = [
            {
                "response": client.get("/api/partto/?partTo={}".format(key)),
                "key": key,
            }
            for key in response.data["partTos"]
        ]
        beans = None
        roast = None
        for partTo in partTos:
            self.assertEqual(partTo["response"].status_code, 200)
            if partTo["response"].data["name"] == "Baked Beans (Easy)":
                beans = partTo["response"].data | {"key": partTo["key"]}
            if partTo["response"].data["name"] == "Bavarian Pot Roast":
                roast = partTo["response"].data | {"key": partTo["key"]}
        response = client.post(
            "/api/run/stage",
            {"partTos": [beans["key"]]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        runState = response.data["runState"]
        response = client.post(
            "/api/run/stage",
            {"runState": runState, "partTos": [roast["key"]]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        runState = response.data["runState"]
        self.assertEqual(response.status_code, 200)
        response = client.post(
            "/api/run/start",
            {"runState": runState},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        runState = response.data["runState"]
        response = client.get("/api/run/?runState={}".format(runState))
        self.assertEqual(response.status_code, 200)
        started = response.data["started"]
        self.assertEqual(len(started), 1)
        response = client.get("/api/task/?task={}".format(started[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["description"], "chop an onion and put it in 4ish cup bowl"
        )

        response = client.post(
            "/api/run/complete",
            {
                "runState": runState,
                "definitions": started,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        runState = response.data["runState"]
        response = client.get("/api/run/?runState={}".format(runState))
        self.assertEqual(response.status_code, 200)
        started = response.data["started"]

        response = client.get("/api/task/?task={}".format(started[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "put oil in dutch oven")
        self.assertEqual(len(started), 1)

        response = client.post(
            "/api/run/complete",
            {
                "runState": runState,
                "definitions": started,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response = client.get("/api/run/?runState={}".format(response.data["runState"]))
        self.assertEqual(response.status_code, 200)
        started = response.data["started"]

        response = client.get("/api/task/?task={}".format(started[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["description"],
            "put the following in the bowl onion bowl: 1/2 tsp ground ginger, "
            + "1/2 tsp pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, "
            + "2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, 3/4 cup "
            + "beer or beef broth, 1 1/4 cup water",
        )

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
