from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("analyze/", views.analyze_folder, name="analyze_folder"),
    path("make-changes/", views.make_changes, name="make_changes"),
]
