from django.urls import path

from etienda import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.categories, name="categories"),
    path("mens_clothing", views.mens_clothing, name="mens_clothing"),
    path("womens_clothing", views.womens_clothing, name="womens_clothing"),
]
