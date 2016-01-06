import os
import unittest
from .compat import tempfile
from pluginmanager.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        """
        Create the file manager, a temporary directory, and
        two empty files cleverly named `one.py` and `two.py`
        """
        self.file_manager = FileManager()
        self.temp_dir = tempfile.TemporaryDirectory()

        file_path_template = os.path.join(self.temp_dir.name, '{}.py')
        self.filepath_one = file_path_template.format('one')
        self.filepath_two = file_path_template.format('two')
        open(self.filepath_one, 'a+').close()
        open(self.filepath_two, 'a+').close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_collect_filepaths(self):
        """
        pass in the temporary directory in to the `collect_filepaths` method
        and then check to see if the filepaths created in the `setUp` function
        are present in the collected filepaths
        """
        filepaths = self.file_manager.collect_filepaths(self.temp_dir.name)
        self.assertIn(self.filepath_one, filepaths)
        self.assertIn(self.filepath_two, filepaths)

    def test_collect_filepaths_with_blacklisted_filepath(self):
        """
        add filepath_one to the blacklisted filepaths and then
        collect the filepaths and verify that filepath_one is NOT
        in the collected filepaths, but filepath_two is.
        """
        self.file_manager.add_blacklisted_filepaths(self.filepath_one)
        filepaths = self.file_manager.collect_filepaths(self.temp_dir.name)
        self.assertIn(self.filepath_two, filepaths)
        self.assertNotIn(self.filepath_one, filepaths)

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

    def test_get_file_filters(self):
        obj_1 = object()
        obj_2 = object()

        def test_filter(file_filters):
            for f in file_filters:
                if f == obj_1:
                    return [obj_1, ]

        self.file_manager.set_file_filters([obj_1, obj_2])
        result = self.file_manager.get_file_filters(test_filter)
        self.assertIn(obj_1, result)
        self.assertNotIn(obj_2, result)

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
