"""Load the KanjiDict2.xml into the database."""

from datetime import datetime
from typing import List
from xml.etree.ElementTree import Element
import argparse
import xml.etree.ElementTree as ET

from libs.db import get_db
from models.kanji import Kanji
from models.kanji_codepoint import KanjiCodepoint
from models.kanji_meaning import KanjiMeaning
from models.kanji_query_code import KanjiQueryCode
from models.kanji_radical import KanjiRadical
from models.kanji_reading import KanjiReading
from models.kanji_reference_daikanwajiten import KanjiReferenceDaikanwajiten
from models.kanji_reference_index import KanjiReferenceIndex
from models.kanji_stroke_miscount import KanjiStrokeMiscount
from models.kanji_to_radical import KanjiToRadical
from models.kanji_variant import KanjiVariant
from models.kanjidict_version import KanjidictVersion


def main():
    """Main"""

    # --- Load args
    kanji_file = get_args()

    # --- Load File
    with open(kanji_file, 'r') as kanji_file_fp:
        tree = ET.parse(kanji_file_fp)

    root = tree.getroot()

    # --- Update Version if Newer

    database_version = root.findtext('header/database_version')
    last_version_query = KanjidictVersion.select().order_by(
        KanjidictVersion.database_version.desc()
    )

    if last_version_query.count() > 0:
        if database_version == last_version_query.limit(1).get().database_version:
            print('Already have the latest kanjidict at version {}'.format(
                database_version))
            # return
    else:
        date_of_creation = root.findtext(
            'header/date_of_creation') or datetime.now().strftime('%Y-%m-%d')
        new_version = KanjidictVersion(
            file_version=root.findtext('header/file_version'),
            database_version=root.findtext('header/database_version'),
            date_of_creation=datetime.strptime(
                date_of_creation, '%Y-%m-%d')
        )
        new_version.save()
        print('Inserted new kanjidict2 version {}'.format(database_version))

    # --- Insert Characters
    database = get_db()
    number_saved = 0
    for char_elem in root.findall('character'):
        with database.atomic():
            process_character(char_elem)
            number_saved += 1

        print('Created kanji: ', char_elem.findtext('literal'))

    print('Total kanji created {}'.format(number_saved))


def get_args() -> str:
    """Get the CLI Args"""

    parser = argparse.ArgumentParser(
        description='Load the kanjidict2.xml to the database.')
    parser.add_argument(
        'kanjidict_file',
        help='The relative path to the kanjiDict2.xml file.'
    )

    return parser.parse_args().kanjidict_file


def process_character(char_ele: Element):
    """Process a character element."""

    # Literal
    literal = char_ele.findtext('literal')

    kanji, _created = Kanji.get_or_create(literal=literal)

    # Codepoint
    get_kanji_codepoints(char_ele, kanji)

    # Radical
    get_kanji_radicals(char_ele, kanji)

    # Misc

    # - Grade
    grade = char_ele.findtext('misc/grade')
    kanji.grade = int(grade) if grade else None

    # - Stroke Count
    kanji.stroke_count = get_kanji_stroke_count(char_ele, kanji)

    # - Variants
    get_kanji_variants(char_ele, kanji)

    # - Frequency
    frequency = char_ele.findtext('misc/freq')
    kanji.frequency = int(frequency) if frequency else None

    # - Radical Name
    kanji.radical_name = char_ele.findtext('misc/rad_name')

    # - JLPT Old
    jlpt_old = char_ele.findtext('misc/jlpt')
    kanji.jlpt_old = int(jlpt_old) if jlpt_old else None

    # Dictionary Number
    get_kanji_dict_numbers(char_ele, kanji)

    # Query Code
    get_kanji_query_code(char_ele, kanji)

    # Readings

    # - Normal Readings
    get_kanji_normal_readings(char_ele, kanji)

    # - Nanori
    get_kanji_nanori(char_ele, kanji)

    # Meanings
    get_kanji_meanings(char_ele, kanji)

    # Save
    kanji.save()


def get_kanji_codepoints(root: Element, kanji: Kanji) -> List[KanjiCodepoint]:
    """Create or get a KanjiCodepoint"""
    codepoints = []
    for cpv in root.findall('codepoint/cp_value'):
        cp_type = cpv.attrib['cp_type']
        cp_value = cpv.text
        codepoint = KanjiCodepoint.get_or_create(
            kanji=kanji,
            cp_value=cp_value,
            cp_type=cp_type
        )
        codepoints.append(codepoint)

    return codepoints


def get_kanji_radicals(root: Element, kanji: Kanji) -> List[KanjiRadical]:
    """Create or get KanjiRadicals"""

    radicals = []
    for rad in root.findall('radical/rad_value'):
        rad_type = rad.attrib['rad_type']
        rad_value = rad.text if rad.text else int(rad.text or 0)

        radical, _created = KanjiRadical.get_or_create(
            rad_type=rad_type,
            rad_value=rad_value
        )

        KanjiToRadical.get_or_create(
            kanji=kanji,
            radical=radical
        )

        radicals.append(radical)
    return radicals


def get_kanji_stroke_count(root: Element, kanji: Kanji) -> int:
    """Create or get the kanji stroke counts"""

    stroke_count = 0
    for i, stroke_count_elem in enumerate(root.findall('misc/stroke_count')):
        if i == 0:
            stroke_count = int(stroke_count_elem.text or 0)
        else:
            KanjiStrokeMiscount.get_or_create(
                kanji=kanji, stroke_count=stroke_count_elem.text)
    return stroke_count


def get_kanji_variants(root: Element, kanji: Kanji) -> List[KanjiVariant]:
    """Create or get the kanji variants"""
    variants = []
    for var in root.findall('misc/variant'):
        var = KanjiVariant.get_or_create(
            kanji=kanji, var_type=var.attrib['var_type'], var_value=var.text)
        variants.append(var)

    return variants


def get_kanji_dict_numbers(root: Element, kanji: Kanji) -> List[KanjiReferenceIndex]:
    """Reference Numbers"""

    references = []
    for dict_ref in root.find('dic_number') or []:

        dr_type = dict_ref.attrib['dr_type']
        reference_index, _created = KanjiReferenceIndex.get_or_create(
            kanji=kanji, reference=dr_type, index_number=dict_ref.text)

        if dr_type == 'moro':
            if 'm_vol' in dict_ref.attrib and 'm_page' in dict_ref.attrib:
                KanjiReferenceDaikanwajiten.get_or_create(
                    kanji_reference_index=reference_index,
                    volume=dict_ref.attrib['m_vol'],
                    page=dict_ref.attrib['m_page']
                )
        references.append(reference_index)

    return references


def get_kanji_query_code(root: Element, kanji: Kanji) -> List[KanjiQueryCode]:
    """Query Codes"""

    query_codes = []
    for query_code in root.find('query_code') or []:

        skip_misclass = None
        if 'skip_misclass' in query_code.attrib:
            skip_misclass = query_code.attrib['skip_misclass']

        kqc = KanjiQueryCode.get_or_create(
            kanji=kanji,
            qc_type=query_code.attrib['qc_type'],
            qc_value=query_code.text,
            skip_misclass=skip_misclass
        )
        query_codes.append(kqc)

    return query_codes


def get_kanji_normal_readings(root: Element, kanji: Kanji) -> List[KanjiReading]:
    """Get the kanji readings."""

    normal_readings = []
    for reading in root.findall('reading_meaning/rmgroup/reading') or []:
        read = KanjiReading.get_or_create(
            kanji=kanji,
            reading=reading.text,
            reading_type=reading.attrib['r_type']
        )
        normal_readings.append(read)

    return normal_readings


def get_kanji_nanori(root: Element, kanji: Kanji) -> List[KanjiReading]:
    """Get the kanji readings related to nanori"""

    nanori_list = []
    for reading in root.findall('reading_meaning/nanori') or []:
        nanori = KanjiReading.get_or_create(
            kanji=kanji,
            reading=reading.text,
            reading_type='nanori'
        )
        nanori_list.append(nanori)

    return nanori_list


def get_kanji_meanings(root: Element, kanji: Kanji) -> List[KanjiMeaning]:
    """Get the kanji meanings"""

    meanings = []
    for meaning in root.findall('reading_meaning/rmgroup/meaning') or []:
        language = 'en'
        if 'm_lang' in meaning.attrib:
            language = meaning.attrib['m_lang']

        mean = KanjiMeaning.get_or_create(
            kanji=kanji,
            lang=language,
            meaning=meaning.text
        )
        meanings.append(mean)

    return meanings


if __name__ == "__main__":
    main()
