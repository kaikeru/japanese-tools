"""The version information of the kanjidict2.xml file."""

from peewee import ForeignKeyField, IntegerField
from models.base import BaseModel
from models.kanji import Kanji


class KanjiStrokeMiscount(BaseModel):
    """Kanji"""

    stroke_count = IntegerField(null=False)
    kanji = ForeignKeyField(
        Kanji,
        backref='stroke_miscounts',
        field='literal',
        db_column='kanji'
    )

    class Meta:
        """Model Meta."""
        table_name = 'kanji_stroke_miscount'
