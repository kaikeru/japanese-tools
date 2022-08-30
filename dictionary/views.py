from curses.ascii import HT
from django.shortcuts import render
from django.http import Http404
from .models import Kanji
from .serializers import KanjiSerializer

def kanji_detail(request, literal):

    try:
        kanji = Kanji.objects.get(literal=literal)
    except:
        raise Http404

    data = KanjiSerializer(kanji, context={"request": request}).data

    return render(request, "dictionary/kanji_detail.html", {"kanji": data})
