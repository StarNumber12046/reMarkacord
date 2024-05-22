from .base import BASE_URL, HEADERS
import requests

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
    
    def get_servers(self):
        response = requests.get(f"{BASE_URL}/users/@me/guilds", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        if response.status_code != 200:
            print(json_response)
            raise RuntimeError("Failed to get servers")
        return [Guild(item["id"], item["name"]) for item in json_response]
    
    def get_channels(self, guild_id):
        print(guild_id)
        response = requests.get(f"{BASE_URL}/guilds/{guild_id}/channels", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        if response.status_code != 200:
            print(json_response)
            raise RuntimeError("Failed to get channels")
        return [{"id": item["id"], "name": item["name"]} for item in json_response if item['type'] == 0]
    
    def get_messages(self, channel_id):
        response = requests.get(f"{BASE_URL}/channels/{channel_id}/messages?limit=50", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        if response.status_code != 200:
            print(json_response)
            raise RuntimeError("Failed to get messages")
        messages = [Message(item["id"], item["content"], item["author"]) for item in json_response]
        return messages
        