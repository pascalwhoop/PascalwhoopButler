import os
import importlib
import unittest
from unittest.mock import Mock
from components import website
from components import config

class TestWebsite(unittest.TestCase):

    """test website component"""

    def setUp(self):
        importlib.reload(website)

    def test_get_path_for_json(self):
        root_p = config.get_config()['website_root']
        pa = website.get_path_for_json()
        self.assertEqual("{}/_data/2018-reading.json".format(root_p), pa)

    def test_ensure_file_exists(self):
        website._ensure_file_exists('foo.swp')
        exists = os.path.exists('foo.swp')
        self.assertTrue(exists)
        os.remove('foo.swp')

    def test_add_summary(self):
        website.get_path_for_json = Mock(return_value='foo2.swp')
        website._add_summary({"foo": "bar"})
        with open('foo2.swp') as file:
            content = file.read()
            self.assertEqual('[{"foo": "bar"}]', content)
        os.remove('foo2.swp')
        


