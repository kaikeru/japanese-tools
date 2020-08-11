"""REST API Middleware"""

from config import get_config

_CONFIG = get_config()

class LimitOffsetProcessor():
    """Process the incoming request to add offset and limits on the query."""

    def process_request(self, req, _resp):
        """Process Request."""

        # Limit
        limit = _CONFIG['max_response_limit']
        if 'limit' in req.params:
            try:
                request_limit = int(req.params['limit'])
                if 0 < request_limit < limit:
                    limit = request_limit
            except ValueError as exp:
                print(exp)
            except TypeError as exp:
                print(exp)
        req.params['limit'] = limit

        # Offset
        offset = 0
        if 'offset' in req.params:
            try:
                request_offset = int(req.params['offset'])
                if offset < request_offset:
                    offset = request_offset
            except ValueError as exp:
                print(exp)

        req.params['offset'] = offset
