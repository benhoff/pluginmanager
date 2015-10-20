import os
import unittest
from pluginmanager.file_filters import FilenameFileFilter


class TestFilenameFileGetter(unittest.TestCase):
    def setUp(self):
        self.file_filter = FilenameFileFilter()

    def test_plugin_valid(self):
        filename = self.file_filter.filenames[0]
        filename = os.path.join('test/dir', filename)
        bad_filename = os.path.join('test/dir/bad.py')
        self.assertTrue(self.file_filter.plugin_valid(filename))
        self.assertFalse(self.file_filter.plugin_valid(bad_filename))

    def test_call(self):
        filepaths = ['valid/path/__init__.py', 'unvalid/dir/blue.py']
        filtered = self.file_filter(filepaths)
        self.assertIn(filepaths[0], filtered)
        self.assertNotIn(filepaths[1], filtered)
