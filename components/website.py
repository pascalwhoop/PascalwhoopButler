import json
import os
from datetime import date

from components import config
web_root = config.get_config()['website_root']

import logging
LOGGER = logging.getLogger(__name__)

def add_json_summary(json_string: str):
    """takes a json summary from mercury and adds it to the websites list of read things

    :json_string: str: TODO
    :returns: TODO

    """
    summary = json.JSONDecoder().decode(json_string)
    summary = process_summary(summary)
    _add_summary(summary)

def process_summary(summary: dict):
    """TODO: Docstring for process_summary.

    :summary: dict: TODO
    :returns: TODO

    """
    del summary['content']
    summary['date_read'] = date.today().isoformat()
    return summary

def _add_summary(summary: dict):
    file_path = get_path_for_json()
    _ensure_file_exists(file_path)
    with open(get_path_for_json(), encoding='utf-8') as json_target_file:
        json_arr = json.load(json_target_file)
        LOGGER.info("current number of articles is: {}".format(len(json_arr)))
        json_arr.append(summary)
    with open(get_path_for_json(), mode='w', encoding='utf-8') as json_target_file:
        json_string = json.dumps(json_arr, ensure_ascii=False)
        json_target_file.write(json_string)
    
def get_path_for_json():
    """TODO: Docstring for get_path_for_json.
    :returns: TODO
    """
    file_name = "{}-reading.json".format(date.today().year)
    path = os.path.join(web_root, '_data')
    os.makedirs(path, exist_ok=True)
    json_path = os.path.join(path, file_name)
    return json_path

def _ensure_file_exists(path):
    if not os.path.exists(path):
        LOGGER.info("generating: {}".format(path))
        with open(path, mode='w', encoding="utf-8") as f:
            f.write('[]')
