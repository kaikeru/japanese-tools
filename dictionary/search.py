from .models import Kanji

def searchKanji(term:str):
    """
    Takes in any search term and searches against the Kotoba
    """

    kanji = Kanji.objects.all().filter(literal__in=term)

    return kanji
