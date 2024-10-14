import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import json


class PartTosTestClass(TestCase):
    def setUp(self):
        self.ids = helpers.loadExamples()
    def test_can_fetch_parttos(self):
        client = Client()
        response = client.get(
            "/api/parttos/"
        )
        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.data)
        self.assertEqual(len(payload['partTos']), 4)
    def test_200s_unknown_parameter(self):
        client = Client()
        response = client.get(
            "/api/parttos/?unknownOne=1".format(self.ids[0])
        )
        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.data)
        self.assertEqual(len(payload['partTos']), 4)
 

