"""The version information of the kanjidict2.xml file."""

from datetime import datetime
from peewee import CharField, DateField, IntegerField, DateTimeField
from models.base import BaseModel

class KanjidictVersion(BaseModel):
    """The version information for the KanjiDict."""
    file_version = IntegerField()
    database_version = CharField(max_length=32)
    date_of_creation = DateField(formats='%Y-%m-%d')
    created_on = DateTimeField(default=datetime.now)

    class Meta:
        """Modle Meta"""
        table_name = 'kanjidict_version'
