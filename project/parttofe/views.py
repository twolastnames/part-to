from django.shortcuts import render
import sys
import os
import re

self_directory = os.path.dirname(os.path.abspath(__file__))
js_directory = "{}/partto/build/static/js".format(self_directory)


print(os.listdir(js_directory))

try:
    shaed_files = {
        re.sub(
            "\.[a-f0-8]{8}", "", filename
        ): "/static/static/js/{}".format(filename)
        for filename in os.listdir(js_directory)
    }
except KeyError:
    print(
        "Can't find front end javascript. Did the project not get built?",
        file=sys.stderr,
    )

import json

print(shaed_files)


def index(request):
    return render(
        request,
        "entry/index.html",
        context={"js_files": shaed_files.values()},
    )
