from django.core.management.base import (
    BaseCommand,
)
from django.test import Client
from parttobe.views.test_nondjango_helpers import get_toml_recipe_as_json
from parttobe.views.parttopost import handle
from collections import namedtuple

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("recipes", nargs="+")

    def handle(self, *args, **options):
        client = Client()
        print(options["recipes"])
        for recipe in options["recipes"]:
            payload = get_toml_recipe_as_json(recipe)
            response = client.post(
                "/api/partto/",
                payload,
                content_type="application/json",
            )
            if response.status_code == 200:
                print(
                    'Recipe "{}" from {} inserted successfully'.format(
                        payload["part_to"]["name"], recipe
                    )
                )
                continue
            print(
                'Recipe from {} failed to insert "{}"'.format(recipe, response.content)
            )
