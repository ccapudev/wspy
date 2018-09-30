import websockets
import http
import re

ROUTERS = [
    # '^/ws/(?P<year>[0-9]{4})/$'
]

ORIGINS = [
    # 'localhost'
]

class ServerProtocol(websockets.WebSocketServerProtocol):

    async def process_request(self, path, request_headers):
        if not any(re.match(regex, path) for regex in ROUTERS):
            return http.HTTPStatus.OK, [], b'Websocket connection only\n'
        else:
            # print('request_headers' ,request_headers)
            return None

    @staticmethod
    def process_origin(headers, origins=None):
        """
        Handle the Origin HTTP request header.

        Raise :exc:`~websockets.exceptions.InvalidOrigin` if the origin isn't
        acceptable.

        """
        origin = headers.get('Origin', '')
        print(headers)
        if origins is not None:
            if not any(re.match(regex, origin) for regex in ORIGINS):
                raise websockets.exceptions.InvalidOrigin(origin)
        return origin


def register_url(uri_regex):
    ROUTERS.append(uri_regex)


def register_origin(origin):
    ORIGINS.append(origin)


__all__ = [
    'register_url',
    'register_origin',
    'ServerProtocol',
    'ORIGINS'
]