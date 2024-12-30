from django.shortcuts import render
import sys
import os
import re
import shutil

file_types = ['css', 'js', 'media']

self_directory = os.path.dirname(os.path.abspath(__file__))

def get_path(type):
    return os.path.join(self_directory, "partto", "build", "static", type)



try:
    raw_files = { type: os.listdir(get_path(type))
        for type in file_types
    }
except:
    print("could not find a type directory")
    files = []


try:
    shaed_files = {
        type: [
            "/static/static/{}/{}".format(type, filename)
            for filename in filenames
        ]
        for type, filenames in raw_files.items()
    }
except KeyError:
    print(
        "Can't find front end javascript or css. Did the project not get built?",
        file=sys.stderr,
    )

import json

media_path = os.path.join(self_directory, "partto", "build", "media")

if not os.path.isdir(media_path):
   os.makedirs(media_path)

for file in os.listdir(get_path('media')):
    shutil.copy(os.path.join(self_directory, "partto", "build", "static", "media",file),
    os.path.join(self_directory, "partto", "build", "media")
    )

def index(*args, **kargs):
    return render(
        args[0],
        "entry/index.html",
        context={
            "js_files" : shaed_files['js'],
            "css_files" : shaed_files['css'],
        },
    )
