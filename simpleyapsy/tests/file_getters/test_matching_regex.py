import os
import re
import unittest
import tempfile
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

    def test_get_plugin_filepaths(self):
        valid = 'plugin_file.py'
        unvalid = 'unvalid.py'
        with tempfile.TemporaryDirectory() as temp_dir:
            valid = os.path.join(temp_dir, valid)
            unvalid = os.path.join(temp_dir, unvalid)
            open(valid, 'a').close()
            open(unvalid, 'a').close()
            filepaths = self.file_getter.get_plugin_filepaths(temp_dir)
        self.assertIn(valid, filepaths)
        self.assertNotIn(unvalid, filepaths)
