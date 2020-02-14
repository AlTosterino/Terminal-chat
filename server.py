import socketio
from aiohttp import web

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def message(sid, data):
    print('GOT MESSAGE')
    await sio.emit('message', data, skip_sid=sid)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=5000)