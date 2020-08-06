"""The version information of the kanjidict2.xml file."""

from peewee import ForeignKeyField
from models.base import BaseModel
from models.kanji import Kanji
from models.kanji_radical import KanjiRadical


class KanjiToRadical(BaseModel):
    """Kanji to radical"""

    kanji = ForeignKeyField(Kanji, backref='kanji', db_column='kanji')
    radical = ForeignKeyField(KanjiRadical, backref='radical', db_column='radical')

    class Meta:
        """Meta Class"""
        table_name = 'kanji_to_radical'
