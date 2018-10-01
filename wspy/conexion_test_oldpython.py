#!/usr/bin/env python

# WS client example
import asyncio
import json
import websockets

@asyncio.coroutine
def hello():
    ws = websockets.connect('ws://localhost:8765/ws/0/')
    try:
        name = input("What's your name? ")
        data = dict(nombre=name)
    except Exception as e:
        yield from ws.send(json.dumps(data))
        print("> {}".format(name))

        greeting = yield from ws.recv()
        print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())