from django.test import TestCase
#from uuid import uuid4, UUID
from .shared import schema_to_typescript


class SchemaToTypescript(TestCase):
    def test_can_simple_dump(self):


