import unittest
from unittest.mock import Mock

from components import mercury


class TestMercury(unittest.TestCase):
    """testing mercury component"""

    def setUp(self):
        self._store_request = mercury.request.urlopen
        mercury.request.urlopen = Mock(return_value=MockResponse())

    def tearDown(self):
        mercury.request.urlopen = self._store_request

    def test_parse_url(self):
        response = mercury.try_parse_url("https://pascalbrokmeier.de/about")
        self.assertEqual("a string", response['fakestring'])


mock_response = '{"fakestring": "a string"}'


class MockResponse(object):
    def __init__(self):
        pass

    def read(self):
        return mock_response.encode()
