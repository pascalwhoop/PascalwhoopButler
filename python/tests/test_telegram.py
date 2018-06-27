import unittest
import re
from components import telegram_conn

class TestTelegram(unittest.TestCase):

    """testing telegram component"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_register_handlers(self):
        regex = re.compile(telegram_conn.url_regex)
        matches = regex.match("http://url-at-the-beginning.de")
        self.assertIsNotNone(matches)
        matches = regex.match("some text first http://url-at-the-beginning.de")
        self.assertIsNotNone(matches)
        matches = regex.match("some text and new line \nhttp://url-at-the-beginning.de")
        self.assertIsNotNone(matches)
        matches = regex.match("not-a-good-url.de")
        self.assertIsNone(matches)

    def test_get_url_from_message_text(self):
        message = """Der Planet steht, das System wankt: Der Klimawandel zeigt sich radikaler denn je
        http://m.faz.net/aktuell/wissen/erde-klima/der-planet-steht-das-system-wankt-der-klimawandel-zeigt-sich-radikaler-denn-je-15545724.html"""

        exptected = "http://m.faz.net/aktuell/wissen/erde-klima/der-planet-steht-das-system-wankt-der-klimawandel-zeigt-sich-radikaler-denn-je-15545724.html"
        url = telegram_conn.get_url_from_message_text(message)
        self.assertEqual(exptected, url)
        
        


        
