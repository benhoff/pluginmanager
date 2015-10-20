import unittest
import re
from pluginmanager.file_filters import MatchingRegexFileFilter


class TestMatchingRegexFileGetter(unittest.TestCase):
    def setUp(self):
        self.file_filter = MatchingRegexFileFilter(re.compile('plugin*'))

    def test_add_regex(self):
        self.file_filter.add_regex_expressions('blue')
        self.assertIn('blue', self.file_filter.regex_expressions)

    def test_set_regex(self):
        previous = self.file_filter.regex_expressions
        self.file_filter.set_regex_expressions('red')
        self.assertIn('red', self.file_filter.regex_expressions)
        self.assertNotIn(previous, self.file_filter.regex_expressions)

    def test_call(self):
        paths = ['fancy/plugin_blue.py', 'test/dir/blah.py']
        filtered = self.file_filter(paths)
        self.assertIn(paths[0], filtered)
        self.assertNotIn(paths[1], filtered)

    def test_plugin_valid(self):
        valid_name = 'my/fancy/plugin_blue.py'
        unvalid_name = 'plugin/fancy/path/but_not.py'
        valid_name = self.file_filter.plugin_valid(valid_name)
        unvalid_name = self.file_filter.plugin_valid(unvalid_name)
        self.assertTrue(valid_name)
        self.assertFalse(unvalid_name)
