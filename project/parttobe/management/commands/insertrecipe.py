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
        parser.add_argument("--no-overwrite", action="store_true")

    def handle(self, *args, **options):
        client = Client()
        has_recipes = client.get("/api/parttos/")
        names = (
            set()
            if "no-overwrite" in options and options["no-overwrite"]
            else set(
                [
                    client.get("/api/partto/?partTo={}".format(id)).data["name"]
                    for id in has_recipes.data["partTos"]
                ]
            )
        )
        for recipe in options["recipes"]:
            payload = get_toml_recipe_as_json(recipe)
            if payload["part_to"]["name"] in names:
                continue
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
