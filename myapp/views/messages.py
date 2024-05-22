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
        if not "current_server" in additional_args.keys():
            raise ValueError("current_server not in additional_args")
        super().__init__(reMarkable, current_view, additional_args)
        self.base = self.additional_args["base"]
        self.current_channel = self.additional_args["current_channel"]
        self.hooks.append(self.message_back_hook)
        self.page = 1
        self.hooks.append(self.send_message_hook)
        self.hooks.append(self.message_next_hook)
        self.hooks.append(self.go_back)
        self.client = Client(Config().get("DISCORD_TOKEN"))
        self.messages = self.client.get_messages(self.current_channel)
        self.pages = self.generate_pages(self.messages)

    def generate_pages(self, messages):
        pages_list = []
        current_page = []
        total_height = 0
        for message in messages:
            text = f"@{message.author_username}: {message.content}"
            lines = textwrap.wrap(text, width=1400//30)
            height = len(lines)*30
            if total_height + height > 1300:
                pages_list.append(current_page)
                current_page = []
                total_height = 0
            current_page.append(lines)
            total_height += height
        if current_page:
            pages_list.append(current_page)
        return pages_list
    
    def paginate(self, pages, page):
        if page != 1:
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
                    value=f"Page {page}/{pages}",
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
        page = self.additional_args.get("page", 1)
        messages_for_page = self.pages[page-1]
        
        self.page = page
        self.paginate(len(self.pages), self.page)
        
        self.rm.add(
            Widget(
                id="back",
                typ="button",
                value="Back",
                justify="right",
                x="95%",
                y="10",
            )
        )
        
        last_height = 300
        new_msgbar = Widget(
            id="new_msgbar",
            typ="textinput",
            justify="left",
            x="10",
            y="200",
            fontsize="30",
            width="90%",
            value="Hi from reMarkable!",
        )
        self.rm.add(new_msgbar)
        for msg_index, message in enumerate(messages_for_page):

            for index, line in enumerate(message):
                last_height += 30
                self.rm.add(
                    Widget(
                        id=f"message_{msg_index}_{index}",
                        typ="label",
                        justify="left",
                        x="10",
                        y=f"{last_height}",
                        fontsize="30",
                        value=line,
                    )
                )
            last_height += 10

    def send_message_hook(self, clicked):
        print("EEEEEEE")
        if clicked and clicked[0].strip() == "new_msgbar":
            print("Sending message...")
            print(self.client.send_message(self.current_channel, clicked[1]))
            self.rm.reset()
            self.additional_args["page"] = 1
            self.display()
    
    def message_next_hook(self, clicked):
        if clicked and clicked[0] == "msg_next":
            self.rm.reset()
            
            self.additional_args["page"] = self.page + 1
            self.display()
            return None
    
    def message_back_hook(self, clicked):
        
        if clicked and clicked[0] == "msg_prev":
            self.rm.reset()
            self.additional_args["page"] = self.page - 1
            self.display()
            return None
    
    def go_back(self, clicked):
        if clicked and clicked[0] == "back":
            channels_mod = importlib.import_module("myapp.views.channels")
            self.rm.reset()
            view = channels_mod.ChannelsView(self.rm, self.current_view, additional_args={"current_server": self.additional_args["current_server"]})
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
