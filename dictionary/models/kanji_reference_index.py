"""The version information of the kanjidict2.xml file."""

from peewee import CharField, ForeignKeyField
from models.base import BaseModel
from models.kanji import Kanji


class KanjiReferenceIndex(BaseModel):
    """Kanji"""

    index_number = CharField(max_length=32, null=False)
    reference = CharField(max_length=32, null=False)
    kanji = ForeignKeyField(
        Kanji,
        backref='reference_indexes',
        field='literal',
        db_column='kanji'
    )

    class Meta:
        """Meta class for model."""
        table_name = 'kanji_reference_index'
