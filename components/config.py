import json
import os

#parsing config on startup
with open('config.json') as json_data:
    config = json.load(json_data)
    config['website_root'] = os.path.expanduser(config['website_root'])
    config['pdf_target_path'] = os.path.expanduser(config['pdf_target_path'])

def get_config():
    return config
