#!/usr/bin/env python3

import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print("< {}".format(name))

    greeting = "Hello {}!".format(name)
    await websocket.send(greeting)
    print("> {}".format(greeting))

start_server = websockets.serve(hello, host='141.63.96.13', port=8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
