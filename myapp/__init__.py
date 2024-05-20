import argparse
import os
from .config import Config
from .scenes import logged_in, not_logged_in

from carta import ReMarkable, Widget


def quit_hook(rm: ReMarkable, clicked):
    print(clicked)
    if clicked and clicked[0] == "back":
            print("Quitting...")
            return "exit"

click_hooks = [quit_hook]

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

    button = Widget(
        id="back",
        typ="button",
        value="back",
        justify="left",
        x="0",
        y="0",
    )
    title = Widget(
        id="title",
        typ="label",
        value="Discord",
        justify="center",
        x= "50%",
        y= "20",
        fontsize="50",
    )
    
    if not config.is_logged_in():
        not_logged_in(rm, click_hooks)
    else:
        logged_in(rm, click_hooks)
        

    rm.add(title)
    rm.add(button)
    while True:
        print("_________________________________________")
        print(click_hooks)
        clicked = rm.display()
    
        for hook in click_hooks:
            print("Calling "+ hook.__name__)
            hook(rm, clicked)

