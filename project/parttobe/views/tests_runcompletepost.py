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

    @freeze_time("2024-03-21 01:23:45", as_arg=True)
    def test_will_not_calculate_in_future_to_run_state_creation(time, self):
        # create a state to reread
        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=540),
        )
        kept_run_state = self.runState
        time.move_to("2024-03-21 01:28:45")
        self.changeState("complete", "boil water in large pot for beans")

        # make another entry
        time.move_to("2024-03-21 02:28:45")
        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=420),
        )
        time.move_to("2024-03-21 02:38:45")
        self.changeState("complete", "boil water in large pot for beans")

        # read from the past
        response = self.client.get("/api/run/?runState={}".format(kept_run_state))
        self.assertEqual(response.data["timers"]["enforced"][0]["duration"], 540.0)

    @freeze_time("2024-03-21 01:23:45", as_arg=True)
    def test_can_calculate_durations_from_previous_runs(time, self):
        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=540),
        )
        time.move_to("2024-03-21 01:28:45")
        self.changeState("complete", "boil water in large pot for beans")

        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertEqual(self.runStateData["duration"], 810.0)
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=420),
        )
        time.move_to("2024-03-21 01:33:45")
        self.changeState("complete", "boil water in large pot for beans")
        self.assertEqual(self.runStateData["duration"], 390.0)

        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertEqual(self.runStateData["duration"], 770.0)
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=380),
        )
        time.move_to("2024-03-21 01:37:45")
        self.changeState("complete", "boil water in large pot for beans")

        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=345),
        )
        time.move_to("2024-03-21 01:41:45")
        self.changeState("complete", "boil water in large pot for beans")

        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertEqual(self.runStateData["duration"], 714.0)
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=324),
        )
        time.move_to("2024-03-21 01:48:45")
        self.changeState("complete", "boil water in large pot for beans")

        # the estimated duration goes away after the 6th
        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=300),
        )
        time.move_to("2024-03-21 01:53:45")
        self.changeState("complete", "boil water in large pot for beans")

        # voids do not effect things
        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=300),
        )
        time.move_to("2024-03-21 02:33:45")
        self.changeState("void", "boil water in large pot for beans")

        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
        )
        self.changeState("start", "boil water in large pot for beans")
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=300),
        )

    @freeze_time("2024-03-21 01:23:45")
    def test_can_calculate_endtimes(self):
        self.startPartTos(
            "Frozen Green Beans",
            "Corn on the Cob",
        )
        self.assertEqual(self.runStateData["duration"], 950)
        self.assertStartedDescriptions("wash the corn")
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.assertTimerDescriptions(
            "laxed",
            "wash the corn",
        )
        self.assertTimerDescriptions(
            "enforced",
        )
        self.assertTimerDurations(
            "laxed",
            timedelta(seconds=60),
        )
        self.assertTimerDurations(
            "enforced",
        )
        self.assertImminentTills(
            timedelta(seconds=0),
            timedelta(seconds=0),
        )

        self.changeState("start", "boil water in large pot for beans")
        self.assertEqual(self.runStateData["duration"], 950)
        self.assertStartedDescriptions(
            "boil water in large pot for beans",
            "wash the corn",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for corn",
        )

        self.assertTimerDescriptions(
            "laxed",
            "wash the corn",
        )
        self.assertTimerDescriptions("enforced", "boil water in large pot for beans")
        self.assertTimerDurations(
            "laxed",
            timedelta(seconds=60),
        )
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=540),
        )

        self.assertImminentTills(
            timedelta(seconds=0),
        )

        self.changeState("start", "boil water in large pot for corn")
        self.assertEqual(self.runStateData["duration"], 1010)
        self.assertStartedDescriptions(
            "boil water in large pot for beans",
            "boil water in large pot for corn",
            "wash the corn",
        )
        self.assertTimerDescriptions("imminent")

        self.assertTimerDescriptions(
            "laxed",
            "wash the corn",
        )
        self.assertTimerDescriptions(
            "enforced",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.assertTimerDurations(
            "laxed",
            timedelta(seconds=60),
        )
        self.assertTimerDurations(
            "enforced",
            timedelta(seconds=480),
            timedelta(seconds=540),
        )

        self.assertImminentTills()

        self.changeState("complete", "wash the corn")
        self.assertEqual(self.runStateData["duration"], 950)
        self.assertStartedDescriptions(
            "boil water in large pot for beans",
            "boil water in large pot for corn",
            "cut partially with kitchen shears to weaken cob middle to break in half",
        )
        self.assertTimerDescriptions("imminent")
        self.assertImminentTills()

        self.changeState(
            "complete",
            "cut partially with kitchen shears to weaken cob middle to break in half",
        )
        self.assertEqual(self.runStateData["duration"], 950)
        self.assertStartedDescriptions(
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.assertTimerDescriptions("imminent")
        self.assertImminentTills()

        self.changeState("complete", "boil water in large pot for beans")
        self.assertEqual(self.runStateData["duration"], 770)
        self.assertStartedDescriptions(
            "boil water in large pot for corn",
        )
        self.assertTimerDescriptions("imminent", "put and leave beans in boiling water")
        self.assertImminentTills(timedelta(seconds=360))

        self.changeState("complete", "boil water in large pot for corn")
        self.assertEqual(self.runStateData["duration"], 410)
        self.assertStartedDescriptions()
        self.assertTimerDescriptions(
            "imminent",
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.assertImminentTills(timedelta(seconds=0), timedelta(seconds=120))

        self.changeState("start", "put and leave beans in boiling water")
        self.assertEqual(self.runStateData["duration"], 410)
        self.assertStartedDescriptions("put and leave beans in boiling water")
        self.assertTimerDescriptions(
            "imminent",
            "put corn in and boil",
        )
        self.assertImminentTills(timedelta(seconds=120))

        self.changeState("start", "put corn in and boil")
        self.assertEqual(self.runStateData["duration"], 410)
        self.assertStartedDescriptions(
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.assertTimerDescriptions("imminent")
        self.assertImminentTills()

        self.changeState("complete", "put corn in and boil")
        self.assertEqual(self.runStateData["duration"], 410)
        self.assertStartedDescriptions(
            "put and leave beans in boiling water",
            "remove from heat",
        )
        self.assertTimerDescriptions("imminent")
        self.assertImminentTills()

        self.changeState("complete", "put and leave beans in boiling water")
        self.assertEqual(self.runStateData["duration"], 170)
        self.assertStartedDescriptions(
            "remove from heat",
        )
        self.assertTimerDescriptions("imminent", "get water boiling again")
        self.assertImminentTills(timedelta(seconds=0))

        self.changeState("complete", "remove from heat")
        self.assertEqual(self.runStateData["duration"], 150)
        self.assertStartedDescriptions()
        self.assertTimerDescriptions("imminent", "get water boiling again")
        self.assertImminentTills(timedelta(seconds=0))

        self.changeState("start", "get water boiling again")
        self.assertEqual(self.runStateData["duration"], 150)
        self.assertStartedDescriptions("get water boiling again")
        self.assertTimerDescriptions("imminent")
        self.assertImminentTills()

        self.changeState("complete", "get water boiling again")
        self.assertEqual(self.runStateData["duration"], 30)
        self.assertStartedDescriptions("drain and serve beans")
        self.assertTimerDescriptions("imminent")
        self.assertImminentTills()

        self.changeState("complete", "drain and serve beans")
        self.assertEqual(self.runStateData["duration"], 0)
        self.assertStartedDescriptions()
        self.assertTimerDescriptions("imminent")
        self.assertImminentTills()

    def test_can_multitask(self):
        self.startPartTos(
            "Frozen Green Beans",
            "Corn on the Cob",
            "Bavarian Pot Roast",
            "Baked Beans (Easy)",
        )
        self.assertEqual(self.runStateData["duration"], 11875)
        self.assertStartedDescriptions("put oil in dutch oven")
        self.assertTimerDescriptions(
            "imminent",
            "Heat Oven to 325 degrees",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.changeState("complete", "put oil in dutch oven")
        self.assertEqual(self.runStateData["duration"], 11875)
        self.assertStartedDescriptions("chop an onion and put it in 4ish cup bowl")
        self.assertTimerDescriptions(
            "imminent",
            "Heat Oven to 325 degrees",
            "heat oil in dutch oven",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.changeState("void", "chop an onion and put it in 4ish cup bowl")
        self.assertEqual(self.runStateData["duration"], 11875)
        self.assertStartedDescriptions("get pan and put 2 tbs butter in it")

        self.assertTimerDescriptions(
            "imminent",
            "Heat Oven to 325 degrees",
            "heat oil in dutch oven",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
        self.changeState("complete", "get pan and put 2 tbs butter in it")
        self.assertEqual(self.runStateData["duration"], 11875)
        self.assertStartedDescriptions(
            "put the following "
            + "in the bowl onion bowl: 1/2 tsp ground ginger, 1/2 tsp "
            + "pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, "
            + "2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, "
            + "3/4 cup beer or beef broth, 1 1/4 cup water"
        )
        self.assertTimerDescriptions(
            "imminent",
            "Heat Oven to 325 degrees",
            "heat oil in dutch oven",
            "heat pan to medium heat",
            "boil water in large pot for corn",
            "boil water in large pot for beans",
        )
