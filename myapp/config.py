import json
import os

class Config(object):
    def __init__(self):
        self.config = json.load(open(os.expanduser("~/.config/remarkacord/config.json")))

    def get(self, key):
        return self.config.get(key)
    
    def set(self, key, value):
        self.config[key] = value
        json.dump(self.config, open("config.json", "w"))
    
    def is_logged_in(self):
        return "DISCORD_TOKEN" in self.config.keys()
    
    def generate_default(self):
        json.dump({}, open("config.json", "w"))
