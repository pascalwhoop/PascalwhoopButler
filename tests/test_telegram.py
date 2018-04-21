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



        
