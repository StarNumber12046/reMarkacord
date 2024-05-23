from math import trunc
from myapp.config import Config
from myapp.minicord.classes import Client, Guild
from myapp.views.base import BaseView
from carta import ReMarkable, Widget
import time

from myapp.views.channels import ChannelsView
from myapp.views.dms import DMsView


class GuildsView(BaseView):
    def __init__(
        self, reMarkable: ReMarkable, current_view: list, additional_args: dict = {}
    ) -> None:
        super().__init__(reMarkable, current_view, additional_args)
        self.page = 1

        self.client = Client(Config().get("DISCORD_TOKEN"))
        self.guilds = self.client.get_servers()
        self.pages = self.generate_pages([Guild(id="dms", name="Direct Messages")] + self.guilds)
        
    def handle_buttons(self, clicked: tuple):
        return super().handle_buttons(clicked)
    
    def generate_pages(self, guilds):
        max_channels_per_page = 33
        pages_list = []
        current_page = []
        total_height = 0
        for guild in guilds:
            text = f"{guild.name}"
            if total_height + 50 > 1650:
                pages_list.append(current_page)
                current_page = []
                total_height = 0
            current_page.append((text, guild.id))
            total_height += 50
        if current_page:
            pages_list.append(current_page)
        return pages_list
    
    
    def paginate(self, pages, page):
        if page != 1:
            self.rm.add(
                Widget(
                    id="prev",
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
                    id="next",
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
    
    def display(self):
        self.page = self.additional_args.get("page", 1)
        self.rm.add(
            Widget(
                id="exit",
                typ="button",
                value="Exit",
                justify="right",
                x="95%",
                y="10",
            )
        )
        
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
        self.hooks.append(self.server_click_hook)
        self.hooks.append(self.server_next_hook)
        self.hooks.append(self.server_back_hook)

        client = Client(Config().get("DISCORD_TOKEN"))
        print(self.page-1)
        print(len(self.pages))
        page = self.pages[self.page - 1]

        
        self.paginate(len(self.pages), self.page)
        self.rm.add(
            Widget(
                id="guilds",
                typ="label",
                justify="center",
                x="50%",
                y="70",
                fontsize="30",
                value="Choose a server...",
            )
        )
        height = 100
        for index, server in enumerate(page):
            height += 50
            self.rm.add(
                Widget(
                    id=f"guild_{server[1]}",
                    typ="button",
                    justify="center",
                    x="50%",
                    y=f"{height}",
                    fontsize="30",
                    value=server[0],
                )
            )
    
    def server_click_hook(self, clicked: tuple):
        self.rm.reset()

        
        client = Client(Config().get("DISCORD_TOKEN"))
        if clicked and clicked[0] == "guild_dms":
            self.current_server = "dms"

            view = DMsView(self.rm, self.current_view)
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
        for server in self.guilds:
            if clicked and f'guild_{server.id}' == clicked[0]:
                self.current_server = server.id

                view = ChannelsView(self.rm, self.current_view, {"current_server": self.current_server})
                self.current_view.clear()
                self.current_view.append(view)
                view.display()
                break
            
        return None
    

    def server_next_hook(self, clicked):
        if clicked and clicked[0] == "next":
            self.rm.reset()
            
            self.current_view.clear()
            view = GuildsView(self.rm, self.current_view, additional_args={"page":(self.page+1)})
            self.current_view.append(view)
            view.display()
            return None
    
    def server_back_hook(self, clicked):
        if clicked and clicked[0] == "prev":
            self.rm.reset()
            self.current_view.clear()
            view = GuildsView(self.rm, self.current_view, additional_args={"page":(self.page-1)})
            self.current_view.append(view)
            view.display()
            return None
        
