"""The middleware package."""

from typing import List
from middleware.rest_api import LimitOffsetProcessor

def get_middleware() -> List:
    """Return all middleware."""
    return [
        LimitOffsetProcessor()
    ]
