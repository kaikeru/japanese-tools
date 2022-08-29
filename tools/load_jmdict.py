"""Load the KanjiDict2.xml into the database."""

# --- Setup Django environment
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "japanesetools.settings")
django.setup()

# Imports
from datetime import datetime
from typing import List
from xml.etree.ElementTree import Element
import argparse
import xml.etree.ElementTree as ET

from dictionary.models import (
    Kotoba,
    KotobaKanji,
    KotobaMeaningDefinition,
    KotobaMeaningToKanji,
    KotobaMeaningToReading,
    KotobaReading,
    KotobaKanjiToReading,
    KotobaMeaning,
    KotobaMeaningField,
    KotobaMeaningLoanSource,
)


def main():
    """Main"""

    # --- Load args
    kanji_file = get_args()

    # --- Load File
    with open(kanji_file, "r") as kanji_file_fp:
        tree = ET.parse(kanji_file_fp)

    root = tree.getroot()

    # --- Insert Characters
    number_saved = 0
    for char_elem in root.findall("entry"):
        kotoba = process_entry(char_elem)
        number_saved += 1

        readings = [x.value for x in kotoba.kanji.all()]

        if len(readings) == 0:
            readings = [x.value for x in kotoba.kana.all()]

        print("Created kotoba ({}) with {}".format(kotoba.jmdict_sequence, readings))

    print("Total words created {}".format(number_saved))


def get_args() -> str:
    """Get the CLI Args"""

    parser = argparse.ArgumentParser(
        description="Load the kanjidict2.xml to the database."
    )
    parser.add_argument("jmdict_file", help="The relative path to the jmdict.xml file.")

    return parser.parse_args().jmdict_file


def process_entry(entry: Element) -> Kotoba:
    """Process a character element."""

    # The sequency number
    jmdict_sequence = entry.findtext("ent_seq")

    kotoba, _created = Kotoba.objects.get_or_create(jmdict_sequence=jmdict_sequence)

    # Kanji and Readings
    get_kotoba_reading_elements(entry, kotoba)

    return kotoba


def get_kotoba_reading_elements(root: Element, kotoba: Kotoba):
    """Create or get a KotobaKanji"""

    # Kanji
    kanji_list = []
    for k_ele in root.findall("k_ele"):
        value = k_ele.findtext("keb")
        information = k_ele.findtext("ke_inf")
        priority = k_ele.findtext("ke_pri")

        kanji, _created = KotobaKanji.objects.get_or_create(
            kotoba=kotoba, value=value, information=information, priority=priority
        )
        kanji_list.append(kanji)

    # Readings
    readings = []
    for r_ele in root.findall("r_ele"):
        value = r_ele.findtext("reb")
        information = r_ele.findtext("re_inf")
        priority = r_ele.findtext("re_pri")

        reading, _created = KotobaReading.objects.get_or_create(
            kotoba=kotoba, value=value, information=information, priority=priority
        )

        readings.append(reading)

        # Assign the reading to the Kanji

        restrs = r_ele.findall("re_restr")

        if len(restrs) > 0:
            for restr in restrs:
                for kanji in kanji_list:
                    if restr.text == kanji.value:
                        KotobaKanjiToReading.objects.get_or_create(
                            kanji=kanji, reading=reading
                        )
        else:
            for kanji in kanji_list:
                KotobaKanjiToReading.objects.get_or_create(kanji=kanji, reading=reading)

    get_kotoba_meaning_elements(root, kotoba, kanji_list, readings)


def get_kotoba_meaning_elements(
    root: Element,
    kotoba: Kotoba,
    kanji_list: List[KotobaKanji],
    readings: List[KotobaReading],
):

    part_of_speach = None
    old_misc = []
    for s in root.findall("sense"):

        info = s.findtext("s_inf")
        meaning, _created = KotobaMeaning.objects.get_or_create(
            kotoba=kotoba, information=info
        )

        new_misc = get_kotoba_meaning_misc(meaning, s, "misc", "MISC")

        # Preserve the misc for other meanings because that's what they do in the XML file...
        if new_misc:
            old_misc = new_misc
        else:
            for m in old_misc:
                KotobaMeaningField.objects.get_or_create(
                    meaning=meaning, type=m.type, value=m.value
                )

        get_kotoba_meaning_misc(meaning, s, "pos", "PART_OF_SPEECH")

        get_kotoba_meaning_misc(meaning, s, "field", "FIELD")

        get_kotoba_meaning_misc(meaning, s, "dial", "DIALECT")

        get_kotoba_meaning_misc(meaning, s, "dial", "DIALECT")

        for ls in s.findall("lsource"):
            language = ls.attrib["xml:lang"] if "xml:lang" in ls.attrib else "eng"
            type = ls.attrib["ls_type"] if "ls_type" in ls.attrib else None
            word = ls.text

            KotobaMeaningLoanSource.objects.get_or_create(
                meaning=meaning, language=language, type=type, word=word
            )

        for g in s.findall("gloss"):
            type = g.attrib["g_type"] if "g_type" in g.attrib else None
            KotobaMeaningDefinition.objects.get_or_create(
                meaning=meaning, type=type, value=g.text
            )

        stagk_list = s.findall("stagk")
        if len(stagk_list) > 0:
            for stagk in stagk_list:
                value = stagk.text
                for k in kanji_list:
                    if value == k.value:
                        KotobaMeaningToKanji.objects.get_or_create(
                            meaning=meaning, kanji=k
                        )
        else:
            for k in kanji_list:
                KotobaMeaningToKanji.objects.get_or_create(meaning=meaning, kanji=k)

        stagr_list = s.findall("stagr")
        if len(stagr_list) > 0:
            for stagr in stagr_list:
                value = stagr.text
                for r in readings:
                    if value == r.value:
                        KotobaMeaningToReading.objects.get_or_create(
                            meaning=meaning, reading=r
                        )
        else:
            for r in readings:
                KotobaMeaningToReading.objects.get_or_create(meaning=meaning, reading=r)


def get_kotoba_meaning_misc(
    meaning: KotobaMeaning,
    meaningElement: Element,
    fieldElementName: str,
    fieldType: str,
) -> List[KotobaMeaningField]:

    fields = []
    for f in meaningElement.findall(fieldElementName):
        value = f.text.replace("&", "").replace(";", "")
        field, _created = KotobaMeaningField.objects.get_or_create(
            meaning=meaning, type=fieldType, value=value
        )
        fields.append(field)

    return fields


if __name__ == "__main__":
    main()
