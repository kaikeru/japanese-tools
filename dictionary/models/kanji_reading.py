"""The version information of the kanjidict2.xml file."""

from peewee import CharField, ForeignKeyField
from models.base import BaseModel
from models.kanji import Kanji


class KanjiReading(BaseModel):
    """Kanji"""

    reading_type = CharField(max_length=32)
    reading = CharField(max_length=32)
    kanji = ForeignKeyField(
        Kanji,
        backref='readings',
        field='literal',
        db_column='kanji'
    )

    class Meta:
        """Model Meta"""
        table_name = 'kanji_reading'
