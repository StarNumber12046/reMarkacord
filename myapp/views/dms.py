
import importlib
from math import trunc
from myapp.config import Config
from myapp.minicord.classes import Client
from myapp.views.base import BaseView
from carta import ReMarkable, Widget

class DMsView(BaseView):
    def __init__(self, reMarkable: ReMarkable, current_view: list[callable], additional_args: dict = {}) -> None:

        super().__init__(reMarkable, current_view, additional_args)

        self.hooks.append(self.channel_back_hook)
        self.hooks.append(self.channel_next_hook)
        self.hooks.append(self.go_back)
        self.hooks.append(self.channel_click_hook)
        self.page = 1
        self.hooks.append(self.go_back)
        self.client = Client(Config().get("DISCORD_TOKEN"))
        self.dms = self.client.get_dms()
        print(self.dms)
        self.pages = self.generate_pages(self.dms)

    def generate_pages(self, channels):
        max_channels_per_page = 33
        pages_list = []
        current_page = []
        total_height = 0
        for channel in channels:
            text = f"{channel['name']}"
            if total_height + 50 > 1650:
                pages_list.append(current_page)
                current_page = []
                total_height = 0
            current_page.append((text, channel["id"]))
            total_height += 50
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

        self.rm.add(
            Widget(
                id="back",
                typ="button",
                value="<= Back",
                justify="right",
                x="95%",
                y="10",
            )
        )
        
        client = Client(Config().get("DISCORD_TOKEN"))
        self.page = self.additional_args.get("page", 1)
        channels = self.pages[self.page-1]
        self.paginate(len(self.pages), self.page)
        height = 100
        for channel in channels:
            height += 50
            self.rm.add(
                Widget(
                    id=f"channel_{channel[1]}",
                    typ="button",
                    justify="center",
                    x="50%",
                    y=f"{height}",
                    fontsize="30",
                    value=channel[0],
                )
            )
    
    def channel_next_hook(self, clicked):
        if clicked and clicked[0] == "ch_next":
            self.rm.reset()
            
            view = DMsView(self.rm, self.current_view, {"page":(self.page+1)})
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
    
    def channel_back_hook(self, clicked):
        if clicked and clicked[0] == "ch_prev":
            self.rm.reset()
            view = DMsView(self.rm, self.current_view, {"page":(self.page-1)})
            
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
    
    def go_back(self, clicked):
        if clicked and clicked[0] == "back":
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
            view = messages_mod.MessagesView(self.rm, self.current_view, {"base": 0, "current_channel": channel_id, "current_server": "dms"})
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
