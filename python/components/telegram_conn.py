import telegram as t
import re
import telegram.ext as ext
from components import website, mercury, pdf_maker

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
    url = get_url_from_message_text(text)
    if url[-4:] == '.pdf':
        handle_pdf_url(url)
        bot.send_message(chat_id=update.message.chat_id, text="Parsing a pdf file directly")
    else:
        summary = mercury.parse_url(url)
        if summary is not None:
            #TODO call make_pdf
            pdf_maker.mercury_summary_to_pdf(summary)
            pdf_maker.save_website(url, file_name)
            website.add_json_summary(summary)
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

def handle_pdf_url(url):
    #TODO 
    pass

#matching also when url is in later line
url_regex = '((.|\n)*)(http[s]*:\/\/)'
def _register_handlers():
    dispatcher.add_handler(ext.CommandHandler('start', start_handler))
    #from the source code of the framework:
    #match = re.match(self.pattern, update.effective_message.text)
    #return bool(match)
    dispatcher.add_handler(ext.RegexHandler(url_regex, http_url_handler))
