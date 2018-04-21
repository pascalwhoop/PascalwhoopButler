import telegram as t
import re
import telegram.ext as ext
import components.mercury as mercury
import components.website as website

import logging
LOGGER = logging.getLogger(__name__)
# setup the entities used
bot = None
updater = None
dispatcher = None

def init(_token: str):
    #sets these three available to all other functions
    global bot, updater, dispatcher
    bot = t.Bot(token=_token)
    updater = ext.Updater(token=_token)
    dispatcher = updater.dispatcher

    _register_handlers()
    LOGGER.info(bot.get_me())

def start_polling():
    """Starts polling the telegram api for messages
    :returns: TODO

    """
    updater.start_polling()

# create hooks into command events
def start_handler(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def http_url_handler(bot, update):
    if not is_me(update):
        LOGGER.error("NOT ME! {}".format(update.message.from_user.username))
        return
    text = update.message.text
    LOGGER.info("parsing url {}".format(text))
    #TODO do some regex magic (remove spaces etc)
    url = get_url_from_message_text(text)
    summary = mercury.parse_url(url)
    if summary is not None:
        website.add_json_summary(summary)
        #TODO call make_pdf
        #TODO not JSON --> parse first
        bot.send_message(chat_id=update.message.chat_id, text="URL parsed\nTitle: {}".format(summary['title']))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="failed to parse URL")

url_capture_regex = re.compile("(.|\n)*(http[s]*:\/\/[^\s]*)")
def get_url_from_message_text(text: str):
    """matches against a regex and returns the url from the message text
    """
    return url_capture_regex.match(text).group(2)

def is_me(update):
    return update.message.from_user.username == 'pascalwhoop'

#matching also when url is in later line
url_regex = '((.|\n)*)(http[s]*:\/\/)'
def _register_handlers():
    dispatcher.add_handler(ext.CommandHandler('start', start_handler))
    #from the source code of the framework:
    #match = re.match(self.pattern, update.effective_message.text)
    #return bool(match)
    dispatcher.add_handler(ext.RegexHandler(url_regex, http_url_handler))
