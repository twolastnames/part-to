import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client


class RunstartPostTestClass(helpers.ClientTester):
    def test_start_with_imminent_timer(self):
        self.startPartTos(
            "Frozen Green Beans",
        )
        self.assertTimerDescriptions(
            "imminent",
            "boil water in large pot for beans",
        )
