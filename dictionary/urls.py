from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import kanji_detail

# The API URLs are now determined automatically by the router.

urlpatterns = [
    path("kanji/<str:literal>", kanji_detail, name="kanji_detail")
]
