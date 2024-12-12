import parttobe.views.test_helpers as helpers
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
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("complete", "put oil in dutch oven")
        self.assertStartedDescriptions("chop an onion and put it in 4ish cup bowl")
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("void", "chop an onion and put it in 4ish cup bowl")
        self.assertStartedDescriptions(
            "put the following "
            + "in the bowl onion bowl: 1/2 tsp ground ginger, 1/2 tsp "
            + "pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, "
            + "2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, "
            + "3/4 cup beer or beef broth, 1 1/4 cup water"
        )
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState(
            "complete",
            "put the following "
            + "in the bowl onion bowl: 1/2 tsp ground ginger, 1/2 tsp "
            + "pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, "
            + "2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, "
            + "3/4 cup beer or beef broth, 1 1/4 cup water",
        )
        self.assertStartedDescriptions("get pan and put 2 tbs butter in it")
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("complete", "get pan and put 2 tbs butter in it")
        self.assertStartedDescriptions(
            "dice half of a green pepper and a whole yellow onion and combine aside"
        )
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState(
            "complete",
            "dice half of a green pepper and a whole yellow onion and combine aside",
        )
        self.assertStartedDescriptions("grease 3 quart baking pan")
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState(
            "complete",
            "grease 3 quart baking pan",
        )

        self.assertStartedDescriptions(
            "gather and combine 54 oz canned pork and beans, 2 tsp dry mustard, "
            + "2/3 cup brown sugar, 1/4 cup cider vinegar, 4 tbs ketchup, & 1/4 "
            + "cup molasses"
        )
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState(
            "complete",
            "gather and combine 54 oz canned pork and beans, 2 tsp dry mustard, "
            + "2/3 cup brown sugar, 1/4 cup cider vinegar, 4 tbs ketchup, & 1/4 "
            + "cup molasses",
        )

        self.assertStartedDescriptions("wash the corn")
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("complete", "wash the corn")

        self.assertStartedDescriptions(
            "cut partially with kitchen shears to weaken cob middle to break in half"
        )
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState(
            "complete",
            "cut partially with kitchen shears to weaken cob middle to break in half",
        )

        self.assertStartedDescriptions()
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("start", "Heat Oven to 325 degrees")

        self.assertStartedDescriptions("Heat Oven to 325 degrees")
        self.assertImminentDescriptions(
            "heat oil in dutch oven",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("start", "heat oil in dutch oven")

        self.assertStartedDescriptions(
            "heat oil in dutch oven", "Heat Oven to 325 degrees"
        )
        self.assertImminentDescriptions(
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("complete", "heat oil in dutch oven")

        self.assertStartedDescriptions("Heat Oven to 325 degrees")
        self.assertImminentDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("start", "heat pan to medium heat")

        self.assertStartedDescriptions(
            "Heat Oven to 325 degrees", "heat pan to medium heat"
        )
        self.assertImminentDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.changeState("start", "boil water in large pot for corn")

        self.assertStartedDescriptions(
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "boil water in large pot for beans",
        )
        self.changeState("start", "boil water in large pot for corn")

        self.assertStartedDescriptions(
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "boil water in large pot for beans",
        )
        self.changeState("start", "boil water in large pot for corn")

        self.assertStartedDescriptions(
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "boil water in large pot for beans",
        )
        self.changeState("start", "boil water in large pot for beans")

        self.assertStartedDescriptions(
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions(
            "put roast meat in dutch oven and brown all sides",
        )
        self.changeState(
            "start",
            "put roast meat in dutch oven and brown all sides",
        )

        self.assertStartedDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "Heat Oven to 325 degrees",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions()
        self.changeState(
            "complete",
            "Heat Oven to 325 degrees",
        )

        self.assertStartedDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "put 10 slices of bacon on pan and put in oven",
            "heat pan to medium heat",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions()
        self.changeState(
            "complete",
            "heat pan to medium heat",
        )

        self.assertStartedDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "put 10 slices of bacon on pan and put in oven",
            "boil water in large pot for beans",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions("saute diced green peppers and onion")
        self.changeState(
            "complete",
            "boil water in large pot for beans",
        )

        self.assertStartedDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "put 10 slices of bacon on pan and put in oven",
            "boil water in large pot for corn",
        )
        self.assertImminentDescriptions(
            "saute diced green peppers and onion",
            "put and leave beans in boiling water",
        )
        self.changeState(
            "complete",
            "boil water in large pot for corn",
        )

        self.assertStartedDescriptions(
            "put roast meat in dutch oven and brown all sides",
            "put 10 slices of bacon on pan and put in oven",
        )
        self.assertImminentDescriptions(
            "saute diced green peppers and onion",
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.changeState(
            "complete",
            "put 10 slices of bacon on pan and put in oven",
        )

        self.assertStartedDescriptions(
            "put roast meat in dutch oven and brown all sides",
        )
        self.assertImminentDescriptions(
            "cook bacon to slightly rare",
            "saute diced green peppers and onion",
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.changeState(
            "complete",
            "put roast meat in dutch oven and brown all sides",
        )

        self.assertStartedDescriptions(
            "dump ingredients in dutch oven and stir",
        )
        self.assertImminentDescriptions(
            "cook bacon to slightly rare",
            "saute diced green peppers and onion",
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.changeState(
            "complete",
            "dump ingredients in dutch oven and stir",
        )

        self.assertStartedDescriptions()
        self.assertImminentDescriptions(
            "reduce heat, cover, and simmer",
            "cook bacon to slightly rare",
            "saute diced green peppers and onion",
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.changeState(
            "start",
            "cook bacon to slightly rare",
        )

        self.assertStartedDescriptions(
            "cook bacon to slightly rare",
        )
        self.assertImminentDescriptions(
            "reduce heat, cover, and simmer",
            "saute diced green peppers and onion",
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.changeState(
            "start",
            "saute diced green peppers and onion",
        )

        self.assertStartedDescriptions(
            "cook bacon to slightly rare",
            "saute diced green peppers and onion",
        )
        self.assertImminentDescriptions(
            "reduce heat, cover, and simmer",
            "put and leave beans in boiling water",
            "put corn in and boil",
        )
        self.changeState(
            "start",
            "put corn in and boil",
        )
