import unittest

from pluginmanager.module_filters import KeywordParser


class TestKeywordParser(unittest.TestCase):
    def setUp(self):
        self.module_filter = KeywordParser()

    def test_get_plugin(self):
        keyword = self.module_filter.keywords[0]
        test_obj = type('', (), {})
        plugins = [test_obj, 5]
        names = [keyword, 'blah']
        plugins = self.module_filter(plugins, names)
        self.assertIn(test_obj, plugins)
        self.assertNotIn(5, plugins)
