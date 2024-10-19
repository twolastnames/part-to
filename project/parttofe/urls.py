from django.urls import path
from . import views
import os
import json


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
    path(route, views.index) for route in get_frontend_routes()
]
