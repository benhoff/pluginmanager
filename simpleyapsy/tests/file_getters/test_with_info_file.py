import unittest
from simpleyapsy.file_getters import WithInfoFileGetter


class TestWithInfoFileGetter(unittest.TestCase):
    def setUp(self):
        self.file_getter = WithInfoFileGetter()

    def test_set_file_extension(self):
        test_extension = 'test'
        self.file_getter.set_file_extensions(test_extension)
        self.assertIn(test_extension, self.file_getter.extensions)

    def test_add_file_extensions(self):
        new_extension = 'test'
        previous_extension = self.file_getter.extensions[0]
        self.file_getter.add_file_extensions(new_extension)
        self.assertIn(new_extension, self.file_getter.extensions)
        self.assertIn(previous_extension, self.file_getter.extensions)

    def test_plugin_valid(self):
        valid_filepath = 'file.yapsy-plugin'
        unvalid_filepath = 'file.bad'
        valid_filepath = self.file_getter.plugin_valid(valid_filepath)
        unvalid_filepath = self.file_getter.plugin_valid(unvalid_filepath)
        self.assertTrue(valid_filepath)
        self.assertFalse(unvalid_filepath)
