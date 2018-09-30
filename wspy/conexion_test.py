#!/usr/bin/env python

# WS client example

import asyncio
import json
import websockets

async def hello():
    async with websockets.connect('ws://localhost:8765') as websocket:
        while True:
            name = input("What's your name? ")
            data = dict(nombre=name)
            await websocket.send(json.dumps(data))
            print(f"> {name}")

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())