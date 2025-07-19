#!/usr/bin/env python3

import os
import toml

self_directory = os.path.dirname(os.path.abspath(__file__))

version = toml.load(os.path.join(self_directory, "..", "version.toml"))["version"]

print("partto_{major}.{minor}.{fix}.{build}-{variant}".format(**version))
