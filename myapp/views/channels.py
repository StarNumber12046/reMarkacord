
import importlib
from math import trunc
from myapp.config import Config
from myapp.minicord.classes import Client
from myapp.views.base import BaseView
from carta import ReMarkable, Widget

class ChannelsView(BaseView):
    def __init__(self, reMarkable: ReMarkable, current_view: list[callable], additional_args: dict = {}) -> None:
        print(f"{additional_args=}")
        if not "base" in additional_args.keys():
            additional_args["base"] = 1
        if not "current_server" in additional_args.keys():
            raise ValueError("current_server not in additional_args")
        super().__init__(reMarkable, current_view, additional_args)
        self.base = self.additional_args["base"]
        self.current_server = self.additional_args["current_server"]
        self.hooks.append(self.channel_back_hook)
        self.hooks.append(self.channel_next_hook)
        self.hooks.append(self.go_back)
        self.hooks.append(self.channel_click_hook)
        self.page = 1
        self.hooks.append(self.go_back)
        self.client = Client(Config().get("DISCORD_TOKEN"))
        self.channels = self.client.get_channels(self.current_server)
        self.pages = self.generate_pages(self.channels)

    def generate_pages(self, channels):
        max_channels_per_page = 33
        pages_list = []
        current_page = []
        total_height = 0
        for channel in channels:
            text = f"{channel["name"]}"
            if total_height + 30 > 1400:
                pages_list.append(current_page)
                current_page = []
                total_height = 0
            current_page.append((text, channel["id"]))
            total_height += 30
        if current_page:
            pages_list.append(current_page)
        return pages_list
    
    def paginate(self, pages, page):
        if page != 1:
            self.rm.add(
                Widget(
                    id="ch_prev",
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
                    id="ch_next",
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
                id="channels",
                typ="label",
                justify="center",
                x="50%",
                y="70",
                fontsize="30",
                value="Choose a channel...",
            )
        )

    def display(self):
        super().display()
        base: int = self.additional_args["base"]
        __import__("os").system("notify-send 'base: " + str(base) + "'")
        print(f"{self.additional_args} LULZ")
        print(f"{base=}")
        
        client = Client(Config().get("DISCORD_TOKEN"))
        self.page = self.additional_args.get("page", 1)
        channels = self.pages[self.page-1]
        
        self.paginate(len(self.pages), self.page)

        for channel in channels:
            self.rm.add(
                Widget(
                    id=f"channel_{channel[1]}",
                    typ="button",
                    justify="center",
                    x="50%",
                    y=f"{100+50*channels.index(channel)}",
                    fontsize="30",
                    value=channel[0],
                )
            )
        base_widget =             Widget(
                id="channel_back",
                typ="button",
                value="<= Back",
                justify="right",
                x=f"0",
                y=f"0", 
            )
        self.rm.add(
            Widget(
                id="channel_back",
                typ="button",
                value="<=",
                justify="left",
                x=f"{1404-50}",
                y=f"10", # At the end of the list
            )
        )
    
    def channel_next_hook(self, clicked):
        print(clicked)
        if clicked and clicked[0] == "ch_next":
            print("Hi *4!")
            self.rm.reset()
            
            view = ChannelsView(self.rm, self.current_view, {"base":(self.page+1)*34, "current_server": self.current_server})
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
    
    def channel_back_hook(self, clicked):
        if clicked and clicked[0] == "ch_prev":
            self.rm.reset()
            view = ChannelsView(self.rm, self.current_view, {"base":(self.page-1)*34, "current_server": self.current_server})
            
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
    
    def go_back(self, clicked):
        if clicked and clicked[0] == "channel_back":
            guilds_mod = importlib.import_module("myapp.views.guilds")
            self.rm.reset()
            view = guilds_mod.GuildsView(self.rm, self.current_view)
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
    
    def channel_click_hook(self, clicked):
        if clicked and clicked[0].startswith("channel_"):
            if clicked[0] == "channel_back":
                return None
            channel_id = int(clicked[0].split("_")[-1])
            self.rm.reset()
            messages_mod = importlib.import_module("myapp.views.messages")
            view = messages_mod.MessagesView(self.rm, self.current_view, {"base": 0, "current_channel": channel_id, "current_server": self.current_server})
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
