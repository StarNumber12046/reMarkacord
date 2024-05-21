from math import trunc
import os
import time
from carta import ReMarkable, Widget

from myapp.config import Config
from myapp.minicord.classes import Client

global servers
servers = [
]

global current_channels
current_channels = [
]

global server_page
server_page = 1
global channel_page
channel_page = 1
global current_server
current_server = 0

def not_logged_in(rm: ReMarkable, hooks: list[callable]):
    rm.add(
        Widget(
            id="login",
            typ="label",
            value="Please login to Discord by setting DISCORD_TOKEN in the config",
            justify="center",
            x="50%",
            y="70",
            fontsize="20",
        )
    )


def server_click_hook(rm: ReMarkable, clicked, config: Config):
    print("Running server_click. ")
    print(clicked)
    rm.reset()
    # THIS CODE IS BUGGED
    # for item in rm.screen:
    #     print(item.id)
    #     if item.id.startswith("guild_"):
    #         rm.remove(item.id)
    
    
    client = Client(config.get("DISCORD_TOKEN"))
    print(servers)
    for server in servers:
    
        if clicked and f'guild_{server["id"]}' == clicked[0]:
            print(server)
            channels = client.get_channels(server["id"])
            print(channels)
            channel_list(rm, server["id"])
            break
    return None


def logged_in(rm: ReMarkable, hooks: list[callable], config: Config, base:int = 0):
    title = Widget(
        id="title",
        typ="label",
        value="Discord",
        justify="center",
        x= "50%",
        y= "20",
        fontsize="50",
    )
    rm.add(title)
    hooks.append(server_click_hook)
    hooks.append(channel_click_hook)
    hooks.append(server_next_hook)
    hooks.append(server_back_hook)
    
    # For later
    hooks.append(channel_next_hook)
    hooks.append(channel_back_hook)
    
    client = Client(config.get("DISCORD_TOKEN"))
    global all_servers
    all_servers = client.get_servers()
    max_servers = len(all_servers)
    num_servers_per_page = 34
    pages = max_servers // num_servers_per_page
    page = trunc(base / num_servers_per_page)
    if base + num_servers_per_page > max_servers:
        servers = all_servers[base:]
    else:
        servers = all_servers[base:base+num_servers_per_page]
    if page != 0:
        rm.add(
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
        rm.add(
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
        rm.add(
            Widget(
                id="page",
                typ="label",
                value=f"Page {page+1}/{pages+1}",
                justify="right",
                x="50%",
                y="100%",
            )
        )
    servers = [{"name": server.name, "id": server.id, "channels": []} for server in all_servers[base:base+34]]
    rm.add(
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
        rm.add(
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
    
def server_click_hook(rm: ReMarkable, clicked, config: Config):
    print("Running server_click. ")
    print(clicked)
    rm.reset()
    # THIS CODE IS BUGGED
    # for item in rm.screen:
    #     print(item.id)
    #     if item.id.startswith("guild_"):
    #         rm.remove(item.id)
    
    
    client = Client(config.get("DISCORD_TOKEN"))
    print(servers)
    for server in all_servers:
        
        if clicked and f'guild_{server.id}' == clicked[0]:
            global current_server
            current_server = server.id
            print(current_server)
            channel_list(rm)
            break

    return None

def channel_list(rm: ReMarkable, base:int = 0):
    client = Client(Config().get("DISCORD_TOKEN"))
    channel_list = client.get_channels(current_server)
    max_channels = len(channel_list)
    num_channels_per_page = 34
    pages = max_channels // num_channels_per_page
    page = trunc(base / num_channels_per_page)
    if base + num_channels_per_page > max_channels:
        channels = channel_list[base:]
    else:
        channels = channel_list[base:base+num_channels_per_page]
    if page != 0:
        rm.add(
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
        rm.add(
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
        rm.add(
            Widget(
                id="page",
                typ="label",
                value=f"Page {page+1}/{pages+1}",
                justify="right",
                x="50%",
                y="100%",
            )
        )
    rm.add(
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
    
    for channel in channels:
        rm.add(
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
    rm.add(
        Widget(
            id="channel_back",
            typ="button",
            value="<==",
            justify="left",
            x="50%",
            y=f"{100+50*len(channels)}", # At the end of the list
        )
    )

def server_next_hook(rm: ReMarkable, clicked, config: Config):
    if clicked and clicked[0] == "next":
        rm.reset()
        logged_in(rm, [], config, base=server_page*34)
        return None

def server_back_hook(rm: ReMarkable, clicked, config: Config):
    if clicked and clicked[0] == "prev":
        rm.reset()
        logged_in(rm, [], config, base=(server_page-1)*34)
        return None
    

def channel_click_hook(rm: ReMarkable, clicked, config: Config):
    print("Running channel_click. ")
    rm.remove("channels")
    if clicked and clicked[0] == "channel_back":
        for server in servers:
            for channel in server["channels"]:
                rm.remove(f"channel_{channel['id']}")
        rm.remove("channel_back")
        logged_in(rm, [], config)
        return None
    print(clicked)
    return None

def channel_next_hook(rm: ReMarkable, clicked, config: Config):
    
    if clicked and clicked[0] == "ch_next":
        rm.reset()
        channels = current_channels[channel_page*34:channel_page*34+33]

        channel_list(rm, base=channel_page*34)
        return None
    
def channel_back_hook(rm: ReMarkable, clicked, config: Config):
    if clicked and clicked[0] == "ch_prev":
        rm.reset()

        channel_list(rm, base=(channel_page-1)*34)
        return None
    