#!/usr/bin/env python

# WS server example
import sys, getopt
import json
import asyncio
import websockets
import logging
from routers import (
    ServerProtocol, register_url, register_origin, ORIGINS
)


logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

conexiones = dict()
USERS = set()


'''
    Configuracion:
    register_url('/path/for/ws/protocol/')
    register_origin('mysite.com.pe')
'''


# Configuracion
register_url('^/ws/0/$')
register_origin('http://devperu.org.pe:8000')
register_origin('')


async def register(websocket, path):
    ''' Metodo que agrega al usuario a un conjunto general 'USERS'
    y los agrupa por path de conexion.
    :param websocket:
    :param path:
    :return: None
    '''
    # print(dir(websocket))
    if conexiones.get(path) is None:
        conexiones[path] = set()
    conexiones[path].add(websocket)
    USERS.add(websocket)


async def unregister(websocket, path):
    conexiones[path].remove(websocket)
    USERS.remove(websocket)


def users_by_path(path):
    for u in conexiones.get(path):
        if u.closed:
            continue
        yield u


def users_active():
    for u in USERS:
        if u.closed:
            continue
        yield u


async def send_data(jsondata, path):
    json_response = json.dumps(jsondata)
    # print("Sending => ",json_response)
    await asyncio.wait([u.send(json_response) for u in users_by_path(path)])


async def main(websocket, path):
    await register(websocket, path)
    while True: # loop para mantener conexión.
        raw_data = await websocket.recv()
        try:
            json_data = json.loads(raw_data)
            await send_data(json_data, path)
            # print("Sending")
        except Exception as e:
            print("Discard Conexion e => ", str(e))
            await unregister(websocket, path)



def main_module(host='localhost', port=8765):
    try:
        start_server = websockets.serve(
            main, host, port, create_protocol=ServerProtocol,
            origins=ORIGINS
        )

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except websockets.exceptions.ConnectionClosed:
        logger.warning("Conexion Closed")
    except KeyboardInterrupt:
        logger.warning("Proceso WebSocket terminado")
    except Exception as e:
        logger.warning("Conexion Interrupted {}".format(e,))


def procesar_argumentos(argv=tuple()):
    host = 'localhost'
    port = 8765
    try:
        opts, args = getopt.getopt(argv,"h:p:",["host=","port="])
    except getopt.GetoptError:
        print('--host=localhost --port=8000')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--help':
            print('--host=localhost --port=8000')
            sys.exit()
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("--host", "-h"):
            host = arg
    register_origin(f'http://{host}:{port}')
    register_origin(f'https://{host}:{port}')
    return host, port


if __name__ == "__main__":
    _host, _port = procesar_argumentos(sys.argv[1:])
    main_module(_host, _port)