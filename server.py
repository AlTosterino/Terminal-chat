import socketio
import argparse
from aiohttp import web


PARSER = argparse.ArgumentParser(description="Simple terminal chat server")
PARSER.add_argument(
    "host",
    type=str,
    nargs="?",
    help="Address of host, default: localhost",
    default="localhost",
)

PARSER.add_argument(
    "port",
    type=int,
    nargs="?",
    help="Host port, default: 5000",
    default=5000,
)

SIO = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
APP = web.Application()
SIO.attach(APP)

USERNAMES = {}

@SIO.event
async def connect(sid, environ):
    print('Connect ', sid)

@SIO.event
async def disconnect(sid):
    global USERNAMES
    USERNAMES.pop(sid, None)
    print('Disconnect ', sid)

@SIO.event
async def is_username_avaiable(sid, data):
    global USERNAMES
    username = USERNAMES.get(sid)
    if not username:
        for key, value in USERNAMES.items():
            if value == data:
                return None
        USERNAMES.setdefault(sid, data)
    else:
        return username
    return USERNAMES.get(sid)

@SIO.event
async def message(sid, data):
    print('GOT MESSAGE')
    await SIO.emit('message', {'username': USERNAMES.get(sid), 'message': data}, skip_sid=sid)

if __name__ == '__main__':
    args = PARSER.parse_args()
    web.run_app(APP, host=args.host, port=args.port)