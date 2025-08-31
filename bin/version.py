#!/usr/bin/env python3
import toml
import os

self_directory = os.path.dirname(os.path.abspath(__file__))


def get_version_string():
    with open(os.path.join(self_directory, "..", "version.toml")) as file:
        data = toml.load(file)
        return "{major}.{minor}.{fix}.{build}-{variant}".format(**data["version"])


if __name__ == "__main__":
    print(get_version_string())
