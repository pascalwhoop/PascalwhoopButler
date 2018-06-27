from components import telegram_conn, mercury, website, pdf_maker, config
import json
import logging

#configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



def startup():
    telegram_conn.start_polling()


#blocks until disconnect
if __name__ == "__main__":
    telegram_conn.init(config.get_config()['telegram'])
    startup()
