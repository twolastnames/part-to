import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import os
import json
from unittest import skip


class RunGetTestClass(helpers.ClientTester):
    def test_having_timers_before_cooking_with_imminent(self):
        self.stagePartTos(
            "Corn on the Cob",
        )
        self.assertTimerDescriptions("imminent", "boil water in large pot for corn")
        self.assertTimerDescriptions("enforced")
        self.assertTimerDescriptions("laxed")

    def test_not_having_timers_before_cooking_with_laxed(self):
        self.stagePartTos(
            "Bavarian Pot Roast",
        )
        self.assertTimerDescriptions("imminent")
        self.assertTimerDescriptions("enforced")
        self.assertTimerDescriptions("laxed")

    skip("the recipe was written wrong")

    def test_keep_roast_in_order(self):
        client = Client()
        file_directory = os.path.dirname(__file__)

        data = helpers.get_toml_recipe_as_json(
            file_directory + "/../mocks_partto/apple_crisp.toml"
        )
        response = client.post(
            "http://testserver/api/partto/",
            json.dumps(data),
            content_type="*",
        )
        self.startPartTos("Apple Crisp", "Bavarian Pot Roast")

        runStateData = self.runStateData
        self.assertUpcomingDescriptions(
            "put oil in dutch oven",
            "chop an onion and put it in 4ish cup bowl",
            "heat oil in dutch oven",
            "put the following in the bowl onion bowl: 1/2 tsp ground ginger, 1/2 tsp pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, 2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, 3/4 cup beer or beef broth, 1 1/4 cup water",
            "put roast meat in dutch oven and brown all sides",
            "dump ingredients in dutch oven and stir",
            "Grease a deep dish pie plate or large baking dish cooking spray and set aside",
            "reduce heat, cover, and simmer",
            "Slice apples in put in a bowl large enough to mix a little with it",
            "Combine sliced apples with other ingredients",
            "Pour the apple mixture into the baking dish",
            "Combine crumble components in a medium dish and stir",
            "Preheat oven to 350 degrees",
            "Melt butter in microwave and stir into crumble until well coated and crumbly",
            "Sprinkle crumble evenly over fruit in baking dish",
            "bake in 350 degree oven for 45-60 minutes until fruit is soft and topping is golden brown",
            "remove meat and slice",
        )
