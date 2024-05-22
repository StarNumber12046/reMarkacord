from math import trunc
from myapp.config import Config
from myapp.minicord.classes import Client
from myapp.views.base import BaseView
from carta import ReMarkable, Widget

from myapp.views.channels import ChannelsView


class GuildsView(BaseView):
    def __init__(
        self, reMarkable: ReMarkable, current_view: list, additional_args: dict = {}
    ) -> None:
        super().__init__(reMarkable, current_view, additional_args)
        if not "base" in additional_args.keys():
            additional_args["base"] = 0
        
    def handle_buttons(self, clicked: tuple):
        return super().handle_buttons(clicked)
    
    def paginate(self, pages, page):
        if page != 0:
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
                    value=f"Page {page+1}/{pages+1}",
                    justify="right",
                    x="50%",
                    y="100%",
                )
            )
    
    def display(self):
        super().display()
        
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
        
        base: int = self.additional_args["base"]
        print(f"{self.additional_args} LULZ")
        print(f"{base=}")
        self.rm.add(title)
        self.hooks.append(self.server_click_hook)
        self.hooks.append(self.server_next_hook)
        self.hooks.append(self.server_back_hook)

        client = Client(Config().get("DISCORD_TOKEN"))

        self.all_servers = client.get_servers()
        max_servers = len(self.all_servers)
        num_servers_per_page = 34
        pages = max_servers // num_servers_per_page
        self.page = trunc(base / num_servers_per_page)
        if base + num_servers_per_page > max_servers:
            servers = self.all_servers[base:]
        else:
            servers = self.all_servers[base : base + num_servers_per_page]

        servers = [
            {"name": server.name, "id": server.id, "channels": []}
            for server in self.all_servers[base : base + 34]
        ]
        
        self.paginate(pages, self.page)
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
        for index, server in enumerate(servers):
            self.rm.add(
                Widget(
                    id=f"guild_{server['id']}",
                    typ="button",
                    justify="center",
                    x="50%",
                    y=f"{50*index + 100}",
                    fontsize="30",
                    value=server["name"],
                )
            )
    
    def server_click_hook(self, clicked: tuple):
        print("Running server_click. ")
        print(clicked)
        self.rm.reset()
        # THIS CODE IS BUGGED
        # for item in rm.screen:
        #     print(item.id)
        #     if item.id.startswith("guild_"):
        #         rm.remove(item.id)
        
        
        client = Client(Config().get("DISCORD_TOKEN"))
        
        for server in self.all_servers:
            if clicked and f'guild_{server.id}' == clicked[0]:
                print("Hi!")
                self.current_server = server.id

                view = ChannelsView(self.rm, self.current_view, {"current_server": self.current_server})
                self.current_view.clear()
                self.current_view.append(view)
                view.display()
                break
            
        return None
    

    def server_next_hook(self, clicked):
        print(clicked)
        if clicked and clicked[0] == "next":
            print("Hi *2!")
            self.rm.reset()
            
            view = GuildsView(self.rm, self.current_view, {"base":(self.page+1)*34})
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
    
    def server_back_hook(self, clicked):
        if clicked and clicked[0] == "prev":
            self.rm.reset()
            view = GuildsView(self.rm, self.current_view, {"base":(self.page-1)*34})
            
            self.current_view.clear()
            self.current_view.append(view)
            view.display()
            return None
        
