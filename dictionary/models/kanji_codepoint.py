"""The version information of the kanjidict2.xml file."""

from peewee import CharField, ForeignKeyField
from models.base import BaseModel
from models.kanji import Kanji


class KanjiCodepoint(BaseModel):
    """Kanji"""

    cp_value = CharField(max_length=32)
    cp_type = CharField(max_length=32)
    kanji = ForeignKeyField(
        Kanji,
        backref='codepoints',
        field='literal',
        db_column='kanji'
    )

    class Meta:
        """Meta info"""
        table_name = 'kanji_codepoint'
