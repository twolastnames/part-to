import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client
import os
import toml


class VersionGetTestClass(TestCase):

    def test_getting_the_version(self):
        client = Client()
        self_directory = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(self_directory, "..", "..", "..", "version.toml")
        versionData = toml.load(filename)
        response = client.get("/api/applicationVersion/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(versionData["version"], response.data)
