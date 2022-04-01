from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("<str:src>/edit", views.edit, name="edit"),
    path("random", views.randomize, name="random"),
    path("search", views.search, name="search"),
    path("<str:src>", views.file, name="src")
]
