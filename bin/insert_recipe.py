#!/usr/bin/env python3
from argparse import ArgumentParser
import sys
import os
from requests import post

sys.path.append(os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), ".."]))
from project.parttobe.views.test_nondjango_helpers import get_toml_recipe_as_json


def get_command_line():
    parser = ArgumentParser()
    parser.add_argument("filename", help="input filename for recipe")
    parser.add_argument("-o", "--origin", help="origin of Part To backend")
    return parser


def insert_recipe(origin, filename):
    dump = get_toml_recipe_as_json(filename)
    response = post("{}/api/partto/".format(origin), json=dump)
    if response.status_code == 200:
        print("recipe inserted successfully")
    print("Post Error:", response.status_code, response.text)


if __name__ == "__main__":
    parser = get_command_line()
    arguments = parser.parse_args()
    print(arguments)
    errors = []
    if not arguments.filename:
        errors.append('missing option "filename"')
    if arguments.origin:
        origin = arguments.origin
    else:
        origin = "http://localhost:8000"
    if len(errors) > 0:
        parser.print_help()
        print("Errors:")
        for message in errors:
            print(message)
        exit(1)
    insert_recipe(origin, arguments.filename)
    # print('o', options, arguments)
