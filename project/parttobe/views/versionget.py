import toml
import os
from dateutil import parser


def handle(arguments):
    self_directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(self_directory, "..", "..", "..", "version.toml")
    versionData = toml.load(filename)["version"]
    versionData["timestamp"] = parser.parse(versionData["timestamp"])
    return versionData
