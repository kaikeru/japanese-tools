from urllib.request import Request
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import KanjiSerializer, KotobaSerializer
from .models import Kanji, Kotoba, KotobaKanji


class KanjiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kanji.objects.all()
    serializer_class = KanjiSerializer


class KotobaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kotoba.objects.all()
    serializer_class = KotobaSerializer


class SearchView(APIView):
    def get(self, request, query, format=None):
        kotoba = [
            x.kotoba
            for x in KotobaKanji.objects.all()
            .filter(value__contains=query)
            .order_by("-priority")[:2]
        ]
        kanji = Kanji.objects.all().filter(literal__in=query).order_by("frequency")[:2]

        returnDict = {
            "kotoba": KotobaSerializer(
                kotoba, many=True, context={"request": request}
            ).data,
            "kanji": KanjiSerializer(kanji, many=True, context={"request": request}).data,
        }
        return Response(
            returnDict
        )
