"""The version information of the kanjidict2.xml file."""

from peewee import CharField, ForeignKeyField
from models.base import BaseModel
from models.kanji_reference_index import KanjiReferenceIndex


class KanjiReferenceDaikanwajiten(BaseModel):
    """Kanji"""

    volume = CharField(max_length=32)
    page = CharField(max_length=32)
    kanji_reference_index = ForeignKeyField(
        KanjiReferenceIndex,
        backref='reference_daikanwajitens'
    )

    class Meta:
        """Model metadata"""
        table_name = 'kanji_reference_daikanwajiten'
