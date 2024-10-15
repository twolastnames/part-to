import toml
from pytimeparse.timeparse import timeparse


def map_definition(key, value):
    if "duration" in value:
        value["duration"] = timeparse(value["duration"])
    return value


def toml_to_body(toml):
    body = {"part_to": toml["part_to"]}
    print("body", body)
    tasks = {k: map_definition(k, v) for (k, v) in toml.items() if k != "part_to"}
    body["tasks"] = [v1 | {"name": k1} for (k1, v1) in tasks.items()]
    return body


def get_toml_recipe_as_json(filename):
    return toml_to_body(toml.load(filename))
