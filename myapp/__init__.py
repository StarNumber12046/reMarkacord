import argparse
import os

import requests

from myapp.views.error import ErrorView
from myapp.views.guilds import GuildsView
from myapp.views.login import LoginView
from myapp.views.nointernet import NoInternetView
from .config import Config

from carta import ReMarkable


def quit_hook(clicked):
    print(clicked)
    if clicked and clicked[0] == "exit":
            print("Quitting...")
            return "exit"



def main():
    config = Config()
    parser = argparse.ArgumentParser(
        prog="myapp",
        description="Example carta application",
    )
    parser.add_argument(
        "--simple-executable",
        help="Path to the simple application",
        action="store",
        default=None,
        dest="simple",
    )
    args = parser.parse_args()

    rm = ReMarkable(simple=args.simple) if args.simple is not None else ReMarkable()

    rm.eclear()
    current_view = []
    try:
        requests.get("https://discord.com")
    except:
        current_view.clear()
        view = NoInternetView(rm, current_view)
        rm.reset()
        current_view.append(view)
        view.display()
        rm.display()
        return
        
    if not config.is_logged_in():
        current_view.clear()
        view = LoginView(rm, current_view)
        view.display()
        current_view.append(view)
        
    else:
        current_view.clear()
        view = GuildsView(rm, current_view)
        view.display()
        current_view.append(view)

    while True:
        print("_________________________________________")
        try:
            clicked = rm.display()

            if quit_hook(clicked) == "exit":
                break
            
            current_view[0].handle_buttons(clicked)
        except:
            current_view.clear()
            view = ErrorView(rm, current_view)
            rm.reset()
            current_view.append(view)
            view.display()


