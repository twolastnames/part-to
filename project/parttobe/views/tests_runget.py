import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client


class RunGetTestClass(helpers.ClientTester):
    def test_not_having_timers_before_cooking_with_imminent(self):
        self.stagePartTos(
            "Corn on the Cob",
        )
        self.assertTimerDescriptions("imminent")
        self.assertTimerDescriptions("enforced")
        self.assertTimerDescriptions("laxed")

    def test_not_having_timers_before_cooking_with_laxed(self):
        self.stagePartTos(
            "Bavarian Pot Roast",
        )
        self.assertTimerDescriptions("imminent")
        self.assertTimerDescriptions("enforced")
        self.assertTimerDescriptions("laxed")
