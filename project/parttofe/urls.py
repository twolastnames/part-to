from django.urls import path, re_path
from . import views
import os
import json
import re


def get_frontend_routes():
    self_directory = os.path.dirname(os.path.abspath(__file__))
    routeFile = os.path.sep.join(
        [self_directory, "partto", "src", "routeKeys.json"]
    )
    with open(routeFile, "r") as file:
        data = json.loads(file.read())
        routes = list(data.values())
        routes.append("")
        return routes


urlpatterns = [
    path(route, views.index)
    for route in get_frontend_routes()
    if ":" not in route
] + [
    re_path(re.sub(r":\w+", "\\\w+", route), views.index)
    for route in get_frontend_routes()
    if ":" in route
]
