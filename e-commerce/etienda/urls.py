from django.urls import path

from etienda import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:category>/", views.category, name="categories"),
    path("products/", views.filter_request, name="products"),
    path("create-product/", views.create_product, name="create_product"),
]
