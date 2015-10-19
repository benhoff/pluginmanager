import os
import unittest
import tempfile
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

    def test_get_plugin_filepath(self):
        filename = self.file_filter.filenames[0]
        with tempfile.TemporaryDirectory() as test_dir:
            file_template = os.path.join(test_dir,
                                         filename)

            python_file = open(file_template, 'w+')
            python_file.write(' ')
            python_file.close()
            files = self.file_filter.get_plugin_filepaths(test_dir)

        self.assertIn(file_template, files)
