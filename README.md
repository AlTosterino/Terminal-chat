![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg) ![Python 3.8](https://upload.wikimedia.org/wikipedia/commons/a/a5/Blue_Python_3.8_Shield_Badge.svg) [![Code Quality](https://www.code-inspector.com/project/4061/score/svg)](https://frontend.code-inspector.com/public/project/4061/Terminal-chat/dashboard) [![Code Grade](https://www.code-inspector.com/project/4061/status/svg)](https://frontend.code-inspector.com/public/project/4061/Terminal-chat/dashboard)
# Python Terminal Chat
Simple asynchronous chat implementation in terminal using python [SocketIO](https://python-socketio.readthedocs.io/en/latest/) and [AIOHTTP](https://docs.aiohttp.org/en/stable/).
## Example
### Client
![Client](https://media.giphy.com/media/SSFA4b83HAAVVWgnnB/giphy.gif)
### Server
![Server](https://media.giphy.com/media/jUbNWjGW6EtsPGxa4b/giphy.gif)
## Getting started
This script and virtual environment uses [Python 3.8.1](https://www.python.org/downloads/release/python-381/)
### Prerequisites
- [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) -> `pip install pipenv`
### Running
> Before running, install dependencies from Pipfile -> `pipenv install`
#### Server
> Server default host is localhost:5000

Usage:
```
usage: server.py [-h] [host] [port]

Simple terminal chat server

positional arguments:
  host        Address of host, default: localhost
  port        Host port, default: 5000

optional arguments:
  -h, --help  show this help message and exit
```
Example: `pipenv run python server.py localhost 5000`

#### Client
> Client default host is localhost:5000

Usage:
```
usage: client.py [-h] [host]

Simple terminal chat client

positional arguments:
  host        Address of host, default: localhost:5000

optional arguments:
  -h, --help  show this help message and exit
```
Example: `pipenv run python client.py localhost:5000`

## Acknowledgments

* Authors of: SocketIO and AIOHTTP

