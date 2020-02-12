import asyncio
import socketio
from time import sleep
from threading import Thread

sio = socketio.AsyncClient()
loop = asyncio.get_event_loop()

@sio.event
async def connect():
    print("I'm connected!")

@sio.event
async def connect_error():
    print("The connection failed!")

@sio.event
async def disconnect():
    print("I'm disconnected!")

async def connect_to_server():
    await sio.connect('http://localhost:5000')
    await sio.wait()

@sio.event
async def message(data):
    print(f"{data:>40}")

async def emit(temp):
    await sio.emit('message', temp)

if __name__ == '__main__':
    t = Thread(target=lambda: loop.run_until_complete(connect_to_server()))
    t.start()
    while True:
        x = input()
        asyncio.run_coroutine_threadsafe(emit(x), loop)