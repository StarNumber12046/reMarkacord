from .base import BASE_URL, HEADERS
import requests

class Guild(object):
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

class Client(object):
    def __init__(self, token) -> None:
        self.token = token
    
    def get_servers(self):
        response = requests.get(f"{BASE_URL}/users/@me/guilds", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        print(json_response)
        return [Guild(item["id"], item["name"]) for item in json_response]
    
    def get_channels(self, guild_id):
        print(guild_id)
        response = requests.get(f"{BASE_URL}/guilds/{guild_id}/channels", headers=HEADERS | {"authorization": self.token})
        json_response = response.json()
        print(json_response)
        return [{"id": item["id"], "name": item["name"]} for item in json_response if item['type'] == 0]
        