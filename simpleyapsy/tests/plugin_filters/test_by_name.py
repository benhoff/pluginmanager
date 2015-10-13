import unittest
from simpleyapsy.plugin_filters import by_name


class NameClass:
    def __init__(self, name='test'):
        self.name = name


class TestByName(unittest.TestCase):
    def test_by_name(self):
        test_name = NameClass('test')
        bogus_name = NameClass('bogus')
        plugins = [test_name, bogus_name]
        plugins = by_name(plugins, 'test')
        self.assertIn(test_name, plugins)
        self.assertNotIn(bogus_name, plugins)
