import socketio
from aiohttp import web

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

USERNAMES = {}

@sio.event
async def connect(sid, environ):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    global USERNAMES
    USERNAMES.pop(sid, None)
    print('disconnect ', sid)

@sio.event
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
    print(USERNAMES)
    return USERNAMES.get(sid)

@sio.event
async def message(sid, data):
    print('GOT MESSAGE')
    await sio.emit('message', {'username': USERNAMES.get(sid), 'message': data}, skip_sid=sid)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=5000)