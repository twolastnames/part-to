from django.urls import path
from . import views

urlpatterns = [
    path("hello-world/", views.hello_world, name="hello_world"),
    path("run/", views.job, name="run"),
    path("job/", views.job, name="job"),
    path("ingredients/", views.ingredients, name="ingredients"),
    path("tools/", views.tools, name="tools"),
]
