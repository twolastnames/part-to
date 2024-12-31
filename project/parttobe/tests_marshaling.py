from django.test import TestCase
from uuid import uuid4, UUID
from parttobe.marshaling import shorten_uuid, recover_uuid


class UrlShortener(TestCase):
    def test_can_echo_uuid(self):
        id = uuid4()
        shorter = shorten_uuid(id)
        recovered = recover_uuid(shorter)
        self.assertEqual(recovered, id)
