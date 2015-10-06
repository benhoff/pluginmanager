import unittest
import re
from simpleyapsy.file_getters import MatchingRegexFileGetter


class TestMatchingRegexFileGetter(unittest.TestCase):
    def setUp(self):
        self.file_getter = MatchingRegexFileGetter(re.compile('plugin*'))

    def test_add_regex(self):
        self.file_getter.add_regex_expressions('blue')
        self.assertIn('blue', self.file_getter.regex_expressions)

    def test_set_regex(self):
        previous = self.file_getter.regex_expressions
        self.file_getter.set_regex_expressions('red')
        self.assertIn('red', self.file_getter.regex_expressions)
        self.assertNotIn(previous, self.file_getter.regex_expressions)

    def test_plugin_valid(self):
        valid_name = 'my/fancy/plugin_blue.py'
        unvalid_name = 'plugin/fancy/path/but_not.py'
        valid_name = self.file_getter.plugin_valid(valid_name)
        unvalid_name = self.file_getter.plugin_valid(unvalid_name)
        self.assertTrue(valid_name)
        self.assertFalse(unvalid_name)
