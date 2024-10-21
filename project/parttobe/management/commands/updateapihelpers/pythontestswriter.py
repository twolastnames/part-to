from .shared import PythonFileWriter

import os

Template = """
import parttobe.views.test_helpers as helpers
from django.test import TestCase
from django.test import Client

class {{ title }}TestClass(TestCase):
    ''' implement your tests here... remove that pass '''
    def test_what_you_want_here_in_{{ slug }}(self):
        self.assertEqual(True, False)
"""


class PythonTestsFileWriter(PythonFileWriter):
    def template(self):
        return Template

    def context(self):
        return {
            "title": self.id.title(),
            "slug": self.id.slug(),
        }

    def filename(self):
        parts = implementation_filename(self.id).split(os.path.sep)
        parts[-1] = "test_{}".format(parts[-1])
        return os.path.sep.join(parts)

    def overwritable(self):
        return False