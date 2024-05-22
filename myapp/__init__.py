import argparse
import os

from myapp.views.guilds import GuildsView
from myapp.views.login import LoginView
from .config import Config

from carta import ReMarkable


def quit_hook(clicked):
    print(clicked)
    if clicked and clicked[0] == "back":
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

        clicked = rm.display()
        rm.screen
        quit_hook(clicked)
        
        current_view[0].handle_buttons(clicked)
        __import__("time").sleep(2)

