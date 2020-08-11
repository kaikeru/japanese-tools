"""The Database manager using PeeWee"""

from peewee import PostgresqlDatabase
from config import get_config


def get_db() -> PostgresqlDatabase:
    """Return the DB object from PeeWee."""

    config = get_config()

    database_conn = PostgresqlDatabase(
        config['db_database'],
        host=config['db_host'],
        user=config['db_user'],
        password=config['db_password'],
    )

    return database_conn
