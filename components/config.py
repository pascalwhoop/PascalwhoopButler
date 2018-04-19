import json

#parsing config on startup
with open('config.json') as json_data:
    config = json.load(json_data)

def get_config():
    return config
