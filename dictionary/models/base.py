"""Base model for the database."""

from peewee import Model
from libs.db import get_db

_DB = get_db()


class BaseModel(Model):
    """The Base model for PeeWee"""
    class Meta:
        """Base Meta Class"""
        database = _DB
