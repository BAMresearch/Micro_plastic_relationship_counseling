#!/usr/bin/env python3

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://141.63.96.13:8765') as websocket:

        name = input("What's your name? ")
        await websocket.send(name)
        print("> {}".format(name))

        greeting = await websocket.recv()
        print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())
