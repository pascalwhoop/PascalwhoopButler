from urllib import request, parse
import json
import logging
from components import config, website, mercury
LOGGER = logging.getLogger(__name__)

consumer_key = config.get_config()['pocket']

urls = {"auth_post": "https://getpocket.com/v3/oauth/request", 
        "get_articles": "https://getpocket.com/v3/get",
        "get_access_token": "https://getpocket.com/v3/oauth/authorize"
       }
headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF8", "X-Accept": "application/json"}


def get_request_token() -> str:
    params = [('consumer_key', consumer_key), ('redirect_uri', 'https://pascalbrokmeier.de')]
    params_bytes = parse.urlencode(params).encode()
    req = request.Request(urls['auth_post'], method="POST", data=params_bytes, headers=headers)
    json_string = request.urlopen(req).read().decode('utf-8')
    return json.JSONDecoder().decode(json_string)['code']


request_token = get_request_token()

def get_access_token() -> str:
    params = [('consumer_key', consumer_key), ('code', request_token)]
    params_bytes = parse.urlencode(params).encode()
    req = request.Request(urls['get_access_token'], method="POST", data=params_bytes, headers=headers)
    json_string = request.urlopen(req).read().decode('utf-8')
    response = json.JSONDecoder().decode(json_string)
    return response['access_token']


def trigger_user_callback():
    input("Press Enter to continue")


def authorize():
    url_to_call = "https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri=https://pascalbrokmeier.de".format(
        request_token=request_token)
    print(url_to_call)
    trigger_user_callback()


def get_article_list(access_token: str):
    params = [('consumer_key', consumer_key), ('access_token', access_token), ('state', 'all'), ('sort', 'newest'),
              ('since', '1492684916')]
    params_bytes = parse.urlencode(params).encode()
    req = request.Request(urls['get_articles'], method="POST", data=params_bytes, headers=headers)
    json_string = request.urlopen(req).read().decode('utf-8')
    #response_json['list'] --> vals --> 'given_url'
    list_dict = json.JSONDecoder().decode(json_string)['list']
    return list_dict.values()


def parse_all_pocket_articles():
    authorize()
    access_token = get_access_token()
    articles = get_article_list(access_token)
    with_issues = []
    for url in [a['given_url'] for a in articles if a['status'] == '0']:
        if website.is_already_parsed(url):
            continue
        summary = mercury.parse_url(url)
        if summary is None:
            with_issues.append(url)
            continue
        website.add_json_summary(summary)
    LOGGER.warning(with_issues)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    parse_all_pocket_articles()
