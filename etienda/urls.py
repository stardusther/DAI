from django.urls import path

from etienda import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("fill_db/", views.fill_database, name="Rellenar base de datos"),
    path("truncate_db/", views.truncate_database, name="Borrar base de datos"),
    path("ejercicio1/", views.ejercicio1, name="Ejercicio 1"),
    path("ejercicio2/", views.ejercicio2, name="Ejercicio 2"),
    path("ejercicio3/", views.ejercicio3, name="Ejercicio 3"),
    path("ejercicio4/", views.ejercicio4, name="Ejercicio 4"),
    path("ejercicio5/", views.ejercicio5, name="Ejercicio 5"),
    path("ejercicio6/", views.ejercicio6, name="Ejercicio 6"),

]