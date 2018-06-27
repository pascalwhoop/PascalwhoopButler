import unittest
from components import pocket
class TestPocket(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_request_token(self):
        token = pocket.get_request_token()
        self.assertIsNotNone(token)
        self.assertTrue(isinstance(token, str))


