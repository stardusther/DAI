from django.urls import path

from etienda import views

urlpatterns = [
    path("", views.index, name="index"),
]