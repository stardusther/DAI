"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from ecommerce import functions as ecommerce_functions
from ecommerce import views as ecommerce_views
from etienda.api import api


urlpatterns = [
    path('', ecommerce_views.redirect_to_store, name='root_redirect'),

    path('etienda/', include('etienda.urls'), name="etienda"),
    path("dump_database/", ecommerce_functions.truncate_database, name="dump_database"),
    path("fill_database/", ecommerce_functions.import_products, name="fill_database"),

    path('admin/', admin.site.urls),
    # path("user/", include("django.contrib.auth.urls")),  # Auth URLS
    path('accounts/', include('allauth.urls')),  # Allouth URLS
    path("api/", api.urls),  # Api URLS
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
