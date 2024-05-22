from math import trunc
from myapp.config import Config
from myapp.minicord.classes import Client
from myapp.views.base import BaseView
from carta import ReMarkable, Widget


class LoginView(BaseView):
    def __init__(self, reMarkable: ReMarkable, current_view: list, additional_args: dict = ...) -> None:
        super().__init__(reMarkable, current_view, additional_args)
    

    def display(self):
        super().display()
        title = Widget(
            id="title",
            typ="label",
            value="Discord",
            justify="center",
            x="50%",
            y="20",
            fontsize="50",
        )
        self.rm.add(title)
        info_message = Widget(
            id="info",
            typ="label",
            value="Please login to Discord by setting DISCORD_TOKEN in the config",
            justify="center",
            x="50%",
            y="70",
            fontsize="30",
        )
        self.rm.add(info_message)
