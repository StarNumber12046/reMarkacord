import importlib
from math import trunc
import textwrap
from myapp.config import Config
from myapp.minicord.classes import Client
from myapp.views.base import BaseView
from carta import ReMarkable, Widget

class MessagesView(BaseView):
    def __init__(self, reMarkable: ReMarkable, current_view: list[callable], additional_args: dict = {}) -> None:
        print(f"{additional_args=}")
        if not "base" in additional_args.keys():
            additional_args["base"] = 1
        if not "current_channel" in additional_args.keys():
            raise ValueError("current_channel not in additional_args")
        super().__init__(reMarkable, current_view, additional_args)
        self.base = self.additional_args["base"]
        self.current_channel = self.additional_args["current_channel"]
        self.hooks.append(self.message_back_hook)
        self.hooks.append(self.message_next_hook)
        self.hooks.append(self.go_back)
        self.page = 0

    def paginate(self, pages, page):
        if page != 0:
            self.rm.add(
                Widget(
                    id="msg_prev",
                    typ="button",
                    value="Back",
                    justify="left",
                    x="0",
                    y="100%",
                )
            )
        if page != pages:
            self.rm.add(
                Widget(
                    id="msg_next",
                    typ="button",
                    value=f"Next",
                    justify="left",
                    x="100%",
                    y="100%",
                )
            )
        if pages != 0:
            self.rm.add(
                Widget(
                    id="page",
                    typ="label",
                    value=f"Page {page+1}/{pages+1}",
                    justify="right",
                    x="50%",
                    y="100%",
                )
            )
        self.rm.add(
            Widget(
                id="messages",
                typ="label",
                justify="center",
                x="50%",
                y="70",
                fontsize="30",
                value="Choose a message...",
            )
        )

    def display(self):
        super().display()
        base: int = self.additional_args["base"]
        __import__("os").system("notify-send 'base: " + str(base) + "'")
        print(f"{self.additional_args} LULZ")
        print(f"{base=}")
        
        client = Client(Config().get("DISCORD_TOKEN"))
        message_list = client.get_messages(self.current_channel)
        max_messages = len(message_list)
        num_messages_per_page = 34
        pages = max_messages // num_messages_per_page
        self.page = trunc(self.base / num_messages_per_page)
        if self.base + num_messages_per_page > max_messages:
            messages = message_list[self.base:]
        else:
            messages = message_list[self.base:self.base+num_messages_per_page]
        
        self.paginate(pages, self.page)

        message_height = 100
        for message in messages:
            text = f"@{message.author_username}: {message.content}"
            lines = textwrap.wrap(text, width=1400//30)
            height = len(lines)*50
            last_height = message_height
            message_height = last_height + 30
            line_height = message_height
            for index, line in enumerate(lines):
                prev_line_height = line_height
                line_height = prev_line_height + 30
                print("Line " + line + "\n Height: " + f"{line_height}")
                self.rm.add(
                    Widget(
                        id=f"message_{message.id}_{index}",
                        typ="label",
                        justify="left",
                        x="10",
                        y=f"{line_height}",
                        fontsize="30",
                        value=line,
                    )
                )
                message_height = line_height
            
        max_messages_per_page = (1400-100)//50
        pages = (max_messages + max_messages_per_page - 1) // max_messages_per_page

        self.rm.add(
            Widget(
                id="message_back",
                typ="button",
                value="<=",
                justify="left",
                x=f"{1404-50}",
                y=f"10", # At the end of the list
            )
        )
    
    def message_next_hook(self, clicked):
        if clicked and clicked[0] == "msg_next":
            self.rm.reset()
            
            view = MessagesView(self.rm, self.current_view, {"base":(self.page+1)*34, "current_channel": self.current_channel})
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
    
    def message_back_hook(self, clicked):
        if clicked and clicked[0] == "msg_prev":
            self.rm.reset()
            view = MessagesView(self.rm, self.current_view, {"base":(self.page-1)*34, "current_channel": self.current_channel})
            
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
    
    def go_back(self, clicked):
        if clicked and clicked[0] == "message_back":
            channels_mod = importlib.import_module("myapp.views.channels")
            self.rm.reset()
            view = channels_mod.ChannelsView(self.rm, self.current_view)
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
