"""The version information of the kanjidict2.xml file."""

from peewee import CharField, ForeignKeyField
from models.base import BaseModel
from models.kanji import Kanji


class KanjiVariant(BaseModel):
    """Kanji"""

    var_value = CharField(max_length=32)
    var_type = CharField(max_length=32)
    kanji = ForeignKeyField(
        Kanji,
        backref='variants',
        field='literal',
        db_column='kanji'
    )

    class Meta:
        """Meta class"""
        table_name = 'kanji_variant'
