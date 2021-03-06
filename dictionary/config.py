"""Get configuration """

from os import getenv
from typing import Dict

def get_config() -> Dict:
    """Load the config and return it."""

    config = {}
    config['db_host'] = getenv('DB_HOST', 'localhost')
    config['db_user'] = getenv('DB_USER', 'postgres')
    config['db_password'] = getenv('DB_PASSWORD', 'example')
    config['db_database'] = getenv('DB_DATABASE', 'dictionary')

    config['max_response_limit'] = int(getenv('MAX_RESPONSE_LIMIT', '20'))

    return config
