"""
japanesetools URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("dictionary/", include("dictionary.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/dictionary/", include("dictionary.urls_api")),
]
