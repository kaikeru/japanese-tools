from django.shortcuts import render
from rest_framework import viewsets
from .serializers import KanjiSerializer, KotobaSerializer
from .models import Kanji, Kotoba

class KanjiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Kanji.objects.all()
    serializer_class=KanjiSerializer

class KotobaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Kotoba.objects.all()
    serializer_class=KotobaSerializer
