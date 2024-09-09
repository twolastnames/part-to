from django.core.management.base import (
    BaseCommand,
)

import toml
import json


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("positional_arg", nargs="+", type=str)

    def handle(self, **options):
        for filename in options["positional_arg"]:
            data = toml.load(filename)
            print(json.dumps(data, indent=2))
