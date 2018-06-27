import logging
from urllib import parse, request
import json

import time

import components.config as config

LOGGER = logging.getLogger(__name__)
url_template = "https://mercury.postlight.com/parser?url={}"


def parse_url(url: str):
    """Takes a url and passes it to mercury parser. Then returns the result from the API

    :url: str: TODO
    :returns: TODO

    """
    trials = 0
    while trials < 3:
        result = try_parse_url(url)
        if result is None:
            trials += 1
        else:
            return result


def try_parse_url(url):
    try:
        req_url = url_template.format(parse.quote_plus(url))
        LOGGER.info("mercury outgoing request -- {}".format(req_url))
        req = request.Request(req_url)
        req.add_header('x-api-key', config.get_config()['mercury'])
        req.add_header('Content-Type', 'application/json')
        response = request.urlopen(req)
        raw_content = response.read()
        LOGGER.info("mercury parsing complete for {}".format(url))
        json_string = raw_content.decode('utf-8')
        summary = json.JSONDecoder().decode(json_string)
        return summary
    except Exception as e:
        LOGGER.error(e)
        LOGGER.warning("might have reached a timeout. waiting a bit")
        LOGGER.warning(url)
        time.sleep(120)
        return None
