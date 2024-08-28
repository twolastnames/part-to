from django.urls import path
from . import views
from . import validation

urlpatterns = [
    path(
        "hello-world/",
        views.hello_world,
        name="hello_world",
    ),
    path("run/", views.run, name="run"),
    validation.path_from_operation_id("job"),
    path(
        "ingredients/",
        views.ingredients,
        name="ingredients",
    ),
    path("tools/", views.tools, name="tools"),
]
