import logging
import telegram as t
import telegram.ext as ext
import components.mercury as mercury
import components.website as website

log = logging.getLogger(__name__)
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
    log.info(bot.get_me())

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
        return
    text = update.message.text
    #TODO do some regex magic (remove spaces etc)
    summary = mercury.parse_url(text)
    website.add_json_summary(summary)

    #TODO call make_pdf

def is_me(update):
    return update.message.from_user.username == 'pascalwhoop'

def _register_handlers():
    dispatcher.add_handler(ext.CommandHandler('start', start_handler))
    dispatcher.add_handler(ext.RegexHandler('http[s]*:\/\/', http_url_handler))
