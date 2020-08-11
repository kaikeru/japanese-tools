"""/kanji"""

from typing import Any, List, Optional, Tuple

import falcon
from falcon import Request, Response

from responses.kanji import get_kanji_response
from models.kanji import Kanji

def get_routes() -> List[Tuple[str, Any]]:
    """Return the routes for this resource."""
    routes = [
        ('/kanji', KanjiResource()),
        ('/kanji/{literal}', KanjiLiteralResource())
    ]

    return routes


class KanjiResource:
    """Kanji endpoint"""

    def on_get(self, req: Request, resp: Response):
        """Handles GET requests"""
        query = Kanji.select()

        query = query.limit(req.params['limit']).offset(req.params['offset'])
        response = []

        for k in query:
            response.append(get_kanji_response(k))

        resp.media = response


class KanjiLiteralResource:
    """Kanji literal"""

    def on_get(self, _req: Request, resp: Response, literal: str):
        """Handles GET requests."""

        kanji: Optional[Kanji] = Kanji.get_or_none(literal=literal)

        if kanji is None:
            raise falcon.HTTPNotFound()

        # --- Return
        resp.media = kanji.get_formatted_response()
