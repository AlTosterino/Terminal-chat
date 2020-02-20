import asyncio
import socketio
import sys
import os
import argparse
from colorama import init, Fore, Style
from time import sleep
from threading import Thread
from multiprocessing import Process

SYSTEM = os.name

# Colorama module init
init()

PARSER = argparse.ArgumentParser(description="Simple terminal chat")
PARSER.add_argument(
    "host",
    type=str,
    nargs="?",
    help="Address of host, default: localhost:5000",
    default="localhost:5000",
)

SIO = socketio.AsyncClient()
LOOP = asyncio.get_event_loop()
USERNAME = None


# * Sync functions


def reset_styles() -> None:
    print(Style.RESET_ALL, end="")


def danger_style() -> str:
    return f"{Style.BRIGHT}{Fore.RED}"


def user_input_style() -> str:
    return f"{Style.BRIGHT}{Fore.GREEN}"


def exit_application() -> None:
    LOOP.call_soon_threadsafe(LOOP.stop)
    os._exit(0)


def clear_screen() -> None:
    os.system("cls" if SYSTEM == "nt" else "clear")


def trying_message() -> None:
    temp = "Trying to connect"
    count = 0
    while True:
        print(temp + "." * count, end="\r")
        count += 1
        sleep(0.1)


def print_reset(text: str, end="\n") -> None:
    """print implementation with Style.RESET_ALL"""
    print(f"{text}{Style.RESET_ALL}", end=end)


def show_user_input(username: str) -> None:
    print_reset(f"{user_input_style()}{username}: ", end="")

def set_user_username(*args) -> None:
    if args:
        global USERNAME
        USERNAME = args[0]
    else:
        print_reset(f'{danger_style()}Username already taken')


# * Async functions


@SIO.event
async def connect():
    # Stop displaying tryin to connect message
    trying_message_process.terminate()
    clear_screen()
    print_reset(f"{Fore.GREEN}Connected!")


@SIO.event
async def connect_error():
    # Stop displaying tryin to connect message
    trying_message_process.terminate()
    print_reset(f"{danger_style()} The connection failed!")


@SIO.event
async def disconnect():
    print_reset(f"{danger_style()} Disconnected!")


@SIO.event
async def message(data) -> None:
    reset_styles()
    print(f"\r{Style.BRIGHT}{Fore.CYAN}{data.get('username')}: {Style.RESET_ALL}{data.get('message')}")
    show_user_input(USERNAME)

async def send_message(message: str) -> None:
    await SIO.emit("message", message)

async def is_username_avaiable(username: str) -> None:
    await SIO.emit('is_username_avaiable', username, callback=set_user_username)


async def connect_to_server(host: str):
    try:
        await SIO.connect(f'http://{host}')
    except socketio.exceptions.ConnectionError:
        # Stop displaying tryin to connect message
        trying_message_process.terminate()
        print_reset(f"{danger_style()}\nDisconnecting... [ConnectionError]")
        exit_application()

    try:
        await SIO.wait()
    except AttributeError:
        print_reset(f"{danger_style()}\nDisconnecting... [ServerWasClosedUnexpected]")
        exit_application()


if __name__ == "__main__":
    args = PARSER.parse_args()
    trying_message_process = Process(target=trying_message)
    trying_message_process.start()
    # Connect to server on separate thread, so user can use terminal
    t = Thread(target=lambda: LOOP.run_until_complete(connect_to_server(args.host)))
    t.start()
    # Get username
    try:
        while True:
            sleep(0.1)
            if not trying_message_process.is_alive():
                if not USERNAME:
                    show_user_input('Pick Your username')
                    new_username = input()
                    if new_username:
                        asyncio.run_coroutine_threadsafe(is_username_avaiable(new_username), LOOP)
                    else:
                        # ANSI Escape
                        print('\033[A', end='')
                else:
                    break
        # Main loop
        while True:
            # Show user input after screen is clear and connected message shown
            sleep(0.1)
            show_user_input(USERNAME)
            user_message = input()
            if user_message:
                asyncio.run_coroutine_threadsafe(send_message(user_message), LOOP)
            else:
                # ANSI Escape
                print('\033[A', end='')
    except KeyboardInterrupt:
        print_reset(f"{danger_style()}\nDisconnecting...")
        exit_application()