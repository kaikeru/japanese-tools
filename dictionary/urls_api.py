from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import KanjiViewSet, KotobaViewSet, SearchView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"kanji", KanjiViewSet, basename="kanji")
router.register(r"kotoba", KotobaViewSet, basename="kotoba")
# The API URLs are now determined automatically by the router.

urlpatterns = [
    path("", include(router.urls)),
    path("search/<str:query>", SearchView.as_view())
]
