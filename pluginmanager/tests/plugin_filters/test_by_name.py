import unittest
from pluginmanager.plugin_filters import NameFilter


class NameClass:
    def __init__(self, name='test'):
        self.name = name


class TestByName(unittest.TestCase):
    def test_by_name(self):
        test_name = NameClass('test')
        bogus_name = NameClass('bogus')
        plugins = [test_name, bogus_name]
        filter_ = NameFilter('test')
        plugins = filter_(plugins)
        self.assertIn(test_name, plugins)
        self.assertNotIn(bogus_name, plugins)
