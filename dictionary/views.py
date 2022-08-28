from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import KanjiSerializer
from .models import Kanji

class KanjiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Kanji.objects.all()
    serializer_class=KanjiSerializer
