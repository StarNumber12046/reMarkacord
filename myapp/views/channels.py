
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
        self.page = 0
        # self.hooks.append(channel_click_hook)
        # self.hooks.append(channel_page_hook)

    def paginate(self, pages, page):
        if page != 0:
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
                    value=f"Page {page+1}/{pages+1}",
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
        channel_list = client.get_channels(self.current_server)
        max_channels = len(channel_list)
        num_channels_per_page = 34
        pages = max_channels // num_channels_per_page
        self.page = trunc(self.base / num_channels_per_page)
        if self.base + num_channels_per_page > max_channels:
            channels = channel_list[self.base:]
        else:
            channels = channel_list[self.base:self.base+num_channels_per_page]
        
        self.paginate(pages, self.page)

        for channel in channels:
            self.rm.add(
                Widget(
                    id=f"channel_{channel['id']}",
                    typ="button",
                    justify="center",
                    x="50%",
                    y=f"{100+50*channels.index(channel)}",
                    fontsize="30",
                    value=channel["name"],
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
