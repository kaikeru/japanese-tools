"""The version information of the kanjidict2.xml file."""

from peewee import CharField, IntegerField
from models.base import BaseModel


class KanjiRadical(BaseModel):
    """Kanji radical"""

    rad_type = CharField(max_length=32)
    rad_value = IntegerField()

    class Meta:
        """Meta info"""
        table_name = 'kanji_radical'
