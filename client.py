import asyncio
import socketio
import sys
from colorama import init, Fore, Style
from time import sleep
from threading import Thread

init()

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
    print(Style.RESET_ALL, end='')
    print('\r' + Fore.RED + 'Someone: ' + Style.RESET_ALL + data)
    print(Fore.GREEN + 'You: ' + Style.RESET_ALL, end='')

async def emit(temp):
    await sio.emit('message', temp)

if __name__ == '__main__':
    t = Thread(target=lambda: loop.run_until_complete(connect_to_server()))
    t.start()
    sleep(1)
    while True:
        x = input(Fore.GREEN + 'You: ' + Style.RESET_ALL)
        asyncio.run_coroutine_threadsafe(emit(x), loop)