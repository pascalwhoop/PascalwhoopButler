from urllib import request, parse
import components.config as config

import logging
LOGGER = logging.getLogger(__name__)
url_template = "https://mercury.postlight.com/parser?url={}"


def parse_url(url: str):
    """Takes a url and passes it to mercury parser. Then returns the result from the API

    :url: str: TODO
    :returns: TODO

    """
    req_url = url_template.format(parse.quote_plus(url))
    req = request.Request(req_url)
    req.add_header('x-api-key', config.get_config()['mercury'])
    req.add_header('Content-Type', 'application/json')
    response = request.urlopen(req)
    raw_content = response.read()
    LOGGER.info("mercury parsing complete for {}".format(url))
    return raw_content.decode('utf-8')
