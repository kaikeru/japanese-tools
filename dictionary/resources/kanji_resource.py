"""/kanji"""

from typing import Any, List, Optional, Tuple, Dict

import falcon

from models.kanji_variant import KanjiVariant
from models.kanji_stroke_miscount import KanjiStrokeMiscount
from models.kanji_reading import KanjiReading
from models.kanji_reference_daikanwajiten import KanjiReferenceDaikanwajiten
from models.kanji_reference_index import KanjiReferenceIndex
from models.kanji_to_radical import KanjiToRadical
from models.kanji_radical import KanjiRadical
from models.kanji_query_code import KanjiQueryCode
from models.kanji_meaning import KanjiMeaning
from models.kanji import Kanji
from models.kanji_codepoint import KanjiCodepoint


def get_routes() -> List[Tuple[str, Any]]:
    """Return the routes for this resource."""
    routes = [
        ('/kanji', KanjiResource()),
        ('/kanji/{literal}', KanjiLiteralResource())
    ]

    return routes


class KanjiResource:
    """Kanji endpoint"""

    def on_get(self, _req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote


class KanjiLiteralResource:
    """Kanji literal"""

    def on_get(self, _req, resp, literal):
        """Handles GET requests."""

        kanji: Optional[Kanji] = Kanji.get_or_none(literal=literal)

        if kanji is None:
            raise falcon.HTTPNotFound()

        resp_payload = {}

        resp_payload['codepoints'] = get_codepoints(kanji)
        resp_payload['frequency'] = kanji.frequency
        resp_payload['grade'] = kanji.grade
        resp_payload['literal'] = kanji.literal
        resp_payload['meanings'] = get_meanings(kanji)
        resp_payload['query_codes'] = get_query_codes(kanji)
        resp_payload['radical_name'] = kanji.radical_name
        resp_payload['radicals'] = get_radicals(kanji)
        resp_payload['readings'] = get_readings(kanji)
        resp_payload['references'] = get_references(kanji)
        resp_payload['strokes'] = get_stroke_counts(kanji)
        resp_payload['variants'] = get_variants(kanji)

        # --- Return
        resp.media = resp_payload


def get_codepoints(kanji: Kanji) -> List[Dict]:
    """Return formated codepoints for a kanji."""
    codepoints = []

    for cps in KanjiCodepoint.select().where(KanjiCodepoint.kanji == kanji.literal):
        single_point = {
            'type': cps.cp_type,
            'value': cps.cp_value
        }
        codepoints.append(single_point)

    return codepoints


def get_meanings(kanji: Kanji) -> Dict[str, List[str]]:
    """Return formated meanings for a kanji."""
    meanings = {}

    for reading in KanjiMeaning.select().where(KanjiMeaning.kanji == kanji.literal):
        if reading.lang in meanings:
            meanings[reading.lang].append(reading.meaning)
        else:
            meanings[reading.lang] = [reading.meaning]

    return meanings


def get_query_codes(kanji: Kanji) -> List[Dict]:
    """Return formated query codes for a kanji."""

    query_codes = []

    for qcs in KanjiQueryCode.select().where(KanjiQueryCode.kanji == kanji.literal):
        single_qc = {
            'type': qcs.qc_type,
            'value': qcs.qc_value
        }

        if qcs.skip_misclass:
            single_qc['skip_misclass'] = qcs.skip_misclass

        query_codes.append(single_qc)

    return query_codes


def get_radicals(kanji: Kanji) -> List[Dict]:
    """Return formated radicals for a kanji."""

    radicals = []
    rad_query = KanjiRadical.select().join(KanjiToRadical).join(
        Kanji).where(Kanji.literal == kanji.literal)
    for rad in rad_query:
        single_rad = {
            'type': rad.rad_type,
            'value': rad.rad_value
        }
        radicals.append(single_rad)

    return radicals


def get_readings(kanji: Kanji) -> Dict[str, List[str]]:
    """Return a dictionary of Lists with the readings."""

    readings = {}

    for reading in KanjiReading.select().where(KanjiReading.kanji == kanji.literal):
        if reading.reading_type in readings:
            readings[reading.reading_type].append(reading.reading)
        else:
            readings[reading.reading_type] = [reading.reading]

    return readings


def get_references(kanji: Kanji) -> List[Dict[str, str]]:
    """Get the kanji references."""

    references = []

    for ref in KanjiReferenceIndex.select().where(KanjiReferenceIndex.kanji == kanji.literal):
        single_ref = {
            'reference': ref.reference,
            'index': ref.index_number
        }

        if ref.reference == 'moro':
            moro_ref = KanjiReferenceDaikanwajiten.get_or_none(
                kanji_reference_index=ref)
            if moro_ref:
                single_ref['moro_info'] = {
                    'volume': moro_ref.volume,
                    'page': moro_ref.page
                }
        references.append(single_ref)

    return references


def get_stroke_counts(kanji: Kanji) -> List:
    """Get the kanji strokes. First one is the correct number and all following are miscounts"""

    strokes = [kanji.stroke_count]

    for miss in KanjiStrokeMiscount.select().where(KanjiStrokeMiscount.kanji == kanji.literal):
        strokes.append(miss.stroke_count)

    return strokes

def get_variants(kanji: Kanji) -> List[Dict[str, str]]:
    """Get the kanji variants"""

    variants = []

    for var in KanjiVariant.select().where(KanjiVariant.kanji == kanji.literal):
        variant_obj = {
            'type': var.var_type,
            'value': var.var_value
        }
        variants.append(variant_obj)

    return variants
