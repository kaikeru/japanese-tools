"""The version information of the kanjidict2.xml file."""

from peewee import CharField, IntegerField
from models.base import BaseModel


class Kanji(BaseModel):
    """Kanji"""

    literal = CharField(max_length=1, primary_key=True)
    grade = IntegerField()
    stroke_count = IntegerField()
    frequency = IntegerField()
    radical_name = CharField(max_length=16)
    jlpt_old = IntegerField()
