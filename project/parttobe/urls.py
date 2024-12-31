from django.urls import path
from . import views
from . import marshaling
from . import endpoints


def get_documented_paths():
    ids = set([endpoints.OperationId(id).name() for id in endpoints.operations.keys()])
    return [marshaling.path_from_operation_id(id) for id in ids]


urlpatterns = []

urlpatterns.extend(get_documented_paths())
