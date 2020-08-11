"""Dictionary Server"""

from wsgiref import simple_server
import falcon
from resources.kanji_resource import get_routes as get_kanji_routes
from middleware import get_middleware


api = falcon.API(
    middleware=get_middleware()
)

routes_v1 = get_kanji_routes()

for route in routes_v1:
    api.add_route('/v1' + route[0], route[1])

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8000
    http = simple_server.make_server('127.0.0.1', PORT, api)
    print('Starting simple server on {}:{}'.format(HOST, PORT))
    http.serve_forever()
