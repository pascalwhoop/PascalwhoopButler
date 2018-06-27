import json
import os
from datetime import date

from components import config
web_root = config.get_config()['website_root']

import logging
LOGGER = logging.getLogger(__name__)

def add_json_summary(summary):
    """takes a json summary from mercury and adds it to the websites list of read things
    """
    summary = process_summary(summary)
    if summary is None:
        return
    _add_summary(summary)

def process_summary(summary: dict):
    """TODO: Docstring for process_summary.

    :summary: dict: TODO
    :returns: TODO

    """
    try:
        del summary['content']
        summary['date_read'] = date.today().isoformat()
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(summary)
        return None
    return summary




def _add_summary(summary: dict):
    file_path = get_path_for_json()
    _ensure_file_exists(file_path)
    json_arr = get_json_summaries()
    json_arr.insert(0, summary)
    with open(get_path_for_json(), mode='w', encoding='utf-8') as json_target_file:
        json_string = json.dumps(json_arr, ensure_ascii=False)
        json_target_file.write(json_string)

def is_already_parsed(url: str):
    _ensure_file_exists(get_path_for_json())
    arr = get_json_summaries()
    url = url.split("?")[0]
    matches = [a for a in arr if url in a['url']]
    return len(matches) > 0

def get_json_summaries():
    with open(get_path_for_json(), encoding='utf-8') as json_target_file:
        json_arr = json.load(json_target_file)
        LOGGER.info("current number of articles is: {}".format(len(json_arr)))
    return json_arr


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
