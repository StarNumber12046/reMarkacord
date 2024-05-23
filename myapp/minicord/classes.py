from .base import BASE_URL, HEADERS
import requests

SERVERS_CACHE = []
CHANNELS_CACHE = {}
SERVER_PROFILES_CACHE = {}


class Guild(object):
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

class Message(object):
    def __init__(self, id, content, user) -> None:
        self.id = id
        self.content = content
        self.author_username = user["username"]

class Client(object):
    def __init__(self, token) -> None:
        self.token = token
        self.user_id = 0
        self.PROFILE = self.get_profile()
        
    def get_profile(self):
        response = requests.get(f"{BASE_URL}/users/@me", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        if response.status_code != 200:

            raise RuntimeError("Failed to get profile")
        self.user_id = json_response["id"]
        return json_response
    def get_server_profile(self, guild_id):
        if guild_id in SERVER_PROFILES_CACHE.keys():
            return SERVER_PROFILES_CACHE[guild_id]
        response = requests.get(f"{BASE_URL}/guilds/{guild_id}/members/{self.user_id}", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        if response.status_code != 200:

            raise RuntimeError("Failed to get server profile")
        SERVER_PROFILES_CACHE[guild_id] = json_response
        return SERVER_PROFILES_CACHE[guild_id]
    
    def get_servers(self):
        if len(SERVERS_CACHE) > 0:
            return SERVERS_CACHE
        response = requests.get(f"{BASE_URL}/users/@me/guilds", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        if response.status_code != 200:

            raise RuntimeError("Failed to get servers")
        SERVERS_CACHE.extend([Guild(item["id"], item["name"]) for item in json_response])
        return SERVERS_CACHE
        
    def can_read_channel(self, overwrites, server_profile, guild_id):
        roles = server_profile["roles"]
        for overwrite in overwrites:
            if int(overwrite["id"]) in roles or int(overwrite["id"]) == self.user_id or int(overwrite["id"]) == guild_id:
                if int(overwrite["allow"]) & (1 << 10) == 1<<10:
                    return True
                if int(overwrite["deny"]) & (1 << 10) == 1<<10:
                    return False
        return True
        
        
    
    def get_channels(self, guild_id):
        if guild_id in CHANNELS_CACHE.keys():
            return CHANNELS_CACHE[guild_id]

        response = requests.get(f"{BASE_URL}/guilds/{guild_id}/channels", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        CHANNELS_CACHE[guild_id] = [{"id": item["id"], "name": item["name"]} for item in json_response if item['type'] == 0 and self.can_read_channel(item["permission_overwrites"], self.get_server_profile(guild_id), guild_id)]
        if response.status_code != 200:

            raise RuntimeError("Failed to get channels")
        return CHANNELS_CACHE[guild_id]
    
    def get_messages(self, channel_id):
        response = requests.get(f"{BASE_URL}/channels/{channel_id}/messages?limit=50", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        if response.status_code != 200:

            raise RuntimeError("Failed to get messages")
        messages = [Message(item["id"], item["content"], item["author"]) for item in json_response]
        return messages
    
    def send_message(self, channel_id, content):
        response = requests.post(f"{BASE_URL}/channels/{channel_id}/messages", headers=HEADERS | {"authorization": self.token}, json={"content": content, "flags": 0})
        json_response = response.json()
        if response.status_code != 200:

            raise RuntimeError("Failed to send message")
        return json_response