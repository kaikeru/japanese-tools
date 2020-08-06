"""The version information of the kanjidict2.xml file."""

from peewee import CharField, ForeignKeyField
from models.base import BaseModel
from models.kanji import Kanji


class KanjiQueryCode(BaseModel):
    """Kanji"""

    qc_value = CharField(max_length=32)
    qc_type = CharField(max_length=32)
    skip_misclass = CharField(max_length=32)
    kanji = ForeignKeyField(
        Kanji,
        backref='query_codes',
        field='literal',
        db_column='kanji'
    )

    class Meta:
        """Model Meta"""
        table_name = 'kanji_query_code'
