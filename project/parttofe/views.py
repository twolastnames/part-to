from django.shortcuts import render
import sys
import os
import re

self_directory = os.path.dirname(os.path.abspath(__file__))
js_directory = os.path.join(self_directory, 'partto', 'build', 'static', 'js')
css_directory = os.path.join(self_directory, 'partto', 'build', 'static', 'css')

try:
    js_files = os.listdir(js_directory)
    css_files = os.listdir(css_directory)
except:
    print("could not find the js directory")
    files = []


try:
    shaed_js_files = {
        re.sub(
            "\.[a-f0-8]{8}", "", filename
        ): "/static/static/js/{}".format(filename)
        for filename in js_files
    }
    shaed_css_files = {
        re.sub(
            "\.[a-f0-8]{8}", "", filename
        ): "/static/static/css/{}".format(filename)
        for filename in css_files
    }
except KeyError:
    print(
        "Can't find front end javascript or css. Did the project not get built?",
        file=sys.stderr,
    )

import json

print('css files', shaed_css_files)
print('js files', shaed_js_files)

def index(*args, **kargs):
    return render(
        args[0],
        "entry/index.html",
        context={
            "js_files": shaed_js_files.values(),
            "css_files": shaed_css_files.values(),
        },
    )
