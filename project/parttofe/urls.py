from django.urls import path
from . import views

urlpatterns = [
    path("/", views.index),
    path("jobpost/", views.index),
    path("job/<str:id>", views.index),
]
