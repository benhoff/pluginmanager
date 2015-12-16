import os
import unittest
from .compat import tempfile
from pluginmanager.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()

    def test_set_file_filters(self):
        current_file_filters = object()
        self.file_manager.add_file_filters(current_file_filters)
        # Create a abstract object for testing
        obj = object()
        self.file_manager.set_file_filters(obj)
        self.assertNotIn(current_file_filters, self.file_manager.file_filters)
        self.assertIn(obj, self.file_manager.file_filters)

    def test_add_file_filters(self):
        test_obj = object()
        self.file_manager.add_file_filters(test_obj)
        self.assertIn(test_obj, self.file_manager.file_filters)

    def test_collect_filepaths(self):
        self.file_manager.file_filters = []
        with tempfile.TemporaryDirectory() as temp_dir:
            file_template = os.path.join(temp_dir, '{}.py')
            file_one = file_template.format('one')
            file_two = file_template.format('two')
            open(file_one, 'a+').close()
            open(file_two, 'a+').close()
            filepaths = self.file_manager.collect_filepaths(temp_dir)

        self.assertIn(file_one, filepaths)

    def test_filter_filepaths(self):
        self.file_manager.file_filters = []
        filepaths = ['test/dir', 'dir/test']
        no_filter = self.file_manager._filter_filepaths(filepaths)
        self.assertEqual(filepaths, no_filter)

        def test_filter(filepaths):
            for filepath in filepaths:
                if filepath == 'test/dir':
                    filepath = [filepath]
                    return filepath

        self.file_manager.add_file_filters(test_filter)
        filtered_filepaths = self.file_manager._filter_filepaths(filepaths)
        self.assertIn('test/dir', filtered_filepaths)
        self.assertNotIn('dir/test', filtered_filepaths)

    def test_blacklist_filepaths(self):
        self.file_manager.set_file_filters([])
        temp_dir = tempfile.TemporaryDirectory()
        file_template = os.path.join(temp_dir.name, '{}.py')
        norm_file = file_template.format('norm')
        blacklist_file = file_template.format('blacklist')
        open(norm_file, 'a+').close()
        open(blacklist_file, 'a+').close()
        self.file_manager.add_blacklisted_filepaths(blacklist_file)
        filepaths = self.file_manager.collect_filepaths(temp_dir.name)
        temp_dir.cleanup()
        self.assertNotIn(blacklist_file, filepaths)
        self.assertIn(norm_file, filepaths)


if __name__ == '__main__':
    unittest.main()
