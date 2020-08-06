"""Kanji Meaning model."""

from peewee import CharField, ForeignKeyField
from models.base import BaseModel
from models.kanji import Kanji


class KanjiMeaning(BaseModel):
    """Kanji meaning"""

    lang = CharField(max_length=16)
    meaning = CharField(max_length=128)
    kanji = ForeignKeyField(
        Kanji,
        backref='meanings',
        field='literal',
        db_column='kanji'
    )

    class Meta:
        """Model Meta"""
        table_name = 'kanji_meaning'
