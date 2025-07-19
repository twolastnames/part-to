from django.test import TestCase
from uuid import uuid4, UUID
from parttobe.serialization import UuidSerialization


class UrlShortener(TestCase):
    def test_can_echo_uuid(self):
        id = uuid4()
        shorter = UuidSerialization().to_representation(id)
        recovered = UuidSerialization().to_internal_value(shorter)
        self.assertEqual(recovered, id)
