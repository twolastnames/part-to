from django.urls import path
from . import views
from . import validation
from . import endpoints


def get_documented_paths():
    ids = set(
        [
            endpoints.OperationId(id).name()
            for id in endpoints.operations.keys()
        ]
    )
    return [validation.path_from_operation_id(id) for id in ids]


#urlpatterns = [
#    path(
#        "hello-world/",
#        views.hello_world,
#        name="hello_world",
#    ),
#    path(
#        "ingredients/",
#        views.ingredients,
#        name="ingredients",
#    ),
#    path("tools/", views.tools, name="tools"),
#]
urlpatterns = []

urlpatterns.extend(get_documented_paths())
