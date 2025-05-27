from django.core.management.base import (
    BaseCommand,
)
from django.test import Client
from parttobe.views.test_nondjango_helpers import get_toml_recipe_as_json
from parttobe.views.parttopost import handle
from collections import namedtuple
import toml
from parttobe.models import TaskDefinition
from parttobe.models import PartTo


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("recipes", nargs="+")

    def handle(self, *args, **options):
        client = Client()
        on = 0
        for filename in options["recipes"]:
            recipe = toml.load(filename)
            name = recipe["part_to"]["name"]
            part_to = PartTo.displayables().get(name=name)
            tasks = part_to.task_definitions
            ids = {}
            for task in tasks:
                on = on + 1
                id = "{}{}".format("task" if task.is_task() else "duty", on)
                ids[task.id] = id
                print("# {}".format(task.description))
                print(
                    "{id} = Definition('{id}', {duration}, {engagement})".format(
                        id=id,
                        duration=task.duration.seconds,
                        engagement=(
                            None if task.is_task() else float(task.engagement) / 100.0
                        ),
                    )
                )
            for task in tasks:
                if not task.depended:
                    continue
                print("{}.depended = {}".format(ids[task.id], ids[task.depended.id]))
            print("line = list(Timeline([{}]))".format(", ".join(ids.values())))

            # payload = get_toml_recipe_as_json(recipe)
