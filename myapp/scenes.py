import os
from carta import ReMarkable, Widget

servers = [
    {"name": "Server 1", "id": 1, "channels": [{"id": 1, "name": "Channel 1"}, {"id": 2, "name": "Channel 2"}]},
    {"name": "Server 2", "id": 2, "channels": [{"id": 3, "name": "Channel 3"}]},
    {"name": "Server 3", "id": 3, "channels": [{"id": 4, "name": "Channel 4"}]},
]


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


def server_click_hook(rm: ReMarkable, clicked):
    print("Running server_click. ")
    print(clicked)
    rm.remove("guilds")
    for item in rm.screen:
        if item.id.startswith("guild_"):
            rm.remove(item.id)
    # for server in servers:
    #     rm.remove(f"guild_{server['id']}")
    # for server in servers:
    #     if f'guild_{server["id"]}' == clicked[0]:
    #         print(server)
    #         channel_list(rm, server["id"])
    #         break
    return None


def logged_in(rm: ReMarkable, hooks: list[callable]):
    hooks.append(server_click_hook)
    hooks.append(channel_click_hook)
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
        

def channel_list(rm: ReMarkable, server_id: int):
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
    for server in servers:
        if server["id"] == server_id:
            for channel in server["channels"]:
                rm.add(
                    Widget(
                        id=f"channel_{channel['id']}",
                        typ="button",
                        justify="center",
                        x="50%",
                        y=f"{100+50*server['channels'].index(channel)}",
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
                    y=f"{100+50*len(server['channels'])}", # At the end of the list
                )
            )
    
def channel_click_hook(rm: ReMarkable, clicked):
    print("Running channel_click. ")
    rm.remove("channels")
    if clicked and clicked[0] == "channel_back":
        for server in servers:
            for channel in server["channels"]:
                rm.remove(f"channel_{channel['id']}")
        rm.remove("channel_back")
        logged_in(rm, [])
        return None
    print(clicked)
    return None