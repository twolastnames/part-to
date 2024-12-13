import parttobe.views.test_helpers as helpers
from freezegun import freeze_time
from datetime import timedelta
from django.test import TestCase
from django.test import Client
import json


class RunCompleteTestClass(helpers.ClientTester):

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

    @freeze_time("2024-03-21 01:23:45")
    def test_can_calculate_endtimes(self):
        self.startPartTos(
            "Frozen Green Beans",
            "Corn on the Cob",
        )
        self.assertStartedDescriptions("wash the corn")
        self.assertImminentDescriptions(
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
            timedelta(seconds=0),
        )

        self.changeState("start", "boil water in large pot for beans")
        self.assertStartedDescriptions(
            "boil water in large pot for beans",
            "wash the corn",
        )
        self.assertImminentDescriptions(
            "boil water in large pot for corn",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )

        self.changeState("start", "boil water in large pot for corn")
        self.assertStartedDescriptions(
            "boil water in large pot for beans",
            "boil water in large pot for corn",
            "wash the corn",
        )
        self.assertImminentDescriptions()
        self.assertImminentTills()

        self.changeState("complete", "wash the corn")
        self.assertStartedDescriptions(
            "boil water in large pot for beans",
            "boil water in large pot for corn",
            "cut partially with kitchen shears to weaken cob middle to break in half",
        )
        self.assertImminentDescriptions()
        self.assertImminentTills()

        self.changeState(
            "complete",
            "cut partially with kitchen shears to weaken cob middle to break in half",
        )
        self.assertStartedDescriptions(
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions()
        self.assertImminentTills()

        self.changeState("complete", "boil water in large pot for beans")
        self.assertStartedDescriptions(
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions("put and leave beans in boiling water")
        self.assertImminentTills(timedelta(seconds=360))

        self.changeState("complete", "boil water in large pot for corn")
        self.assertStartedDescriptions()
        self.assertImminentDescriptions(
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.assertImminentTills(timedelta(seconds=0), timedelta(seconds=120))

        self.changeState("start", "put and leave beans in boiling water")
        self.assertStartedDescriptions("put and leave beans in boiling water")
        self.assertImminentDescriptions(
            "put corn in and boil",
        )
        self.assertImminentTills(timedelta(seconds=120))

        self.changeState("start", "put corn in and boil")
        self.assertStartedDescriptions(
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.assertImminentDescriptions()
        self.assertImminentTills()

        self.changeState("complete", "put corn in and boil")
        self.assertStartedDescriptions(
            "put and leave beans in boiling water",
            "remove from heat",
        )
        self.assertImminentDescriptions()
        self.assertImminentTills()

        self.changeState("complete", "put and leave beans in boiling water")
        self.assertStartedDescriptions(
            "remove from heat",
        )
        self.assertImminentDescriptions("get water boiling again")
        self.assertImminentTills(timedelta(seconds=0))

        self.changeState("complete", "remove from heat")
        self.assertStartedDescriptions()
        self.assertImminentDescriptions("get water boiling again")
        self.assertImminentTills(timedelta(seconds=0))

        self.changeState("start", "get water boiling again")
        self.assertStartedDescriptions("get water boiling again")
        self.assertImminentDescriptions()
        self.assertImminentTills()

        self.changeState("complete", "get water boiling again")
        self.assertStartedDescriptions("drain and serve beans")
        self.assertImminentDescriptions()
        self.assertImminentTills()

        self.changeState("complete", "drain and serve beans")
        self.assertStartedDescriptions()
        self.assertImminentDescriptions()
        self.assertImminentTills()

    def test_can_multitask(self):
        self.startPartTos(
            "Frozen Green Beans",
            "Corn on the Cob",
            "Bavarian Pot Roast",
            "Baked Beans (Easy)",
        )
        self.assertStartedDescriptions("put oil in dutch oven")
        self.assertImminentDescriptions(
            "Heat Oven to 325 degrees",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.changeState("complete", "put oil in dutch oven")
        self.assertStartedDescriptions("chop an onion and put it in 4ish cup bowl")
        self.assertImminentDescriptions(
            "Heat Oven to 325 degrees",
            "heat oil in dutch oven",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.changeState("void", "chop an onion and put it in 4ish cup bowl")
        self.assertStartedDescriptions("get pan and put 2 tbs butter in it")

        self.assertImminentDescriptions(
            "Heat Oven to 325 degrees",
            "heat oil in dutch oven",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.changeState("complete", "get pan and put 2 tbs butter in it")
        self.assertStartedDescriptions(
            "put the following "
            + "in the bowl onion bowl: 1/2 tsp ground ginger, 1/2 tsp "
            + "pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, "
            + "2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, "
            + "3/4 cup beer or beef broth, 1 1/4 cup water"
        )
        self.assertImminentDescriptions(
            "Heat Oven to 325 degrees",
            "heat oil in dutch oven",
            "heat pan to medium heat",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
