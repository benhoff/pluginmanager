import unittest
from .compat import tempfile
from os import path
from pluginmanager.directory_manager import DirectoryManager


class TestDirectoryManager(unittest.TestCase):
    def setUp(self):
        self.directory_manager = DirectoryManager()
        self.directory_manager.set_directories(__file__)

    def test_add_plugin_directory(self):
        test_dir = '/my/plugin/dir'
        self.directory_manager.add_directories(test_dir)
        self.assertIn(test_dir, self.directory_manager.plugin_directories)

    def test_set_plugin_directory(self):
        current_dirs = self.directory_manager.plugin_directories.pop()
        test_dir = '/my/plugin/dir'
        self.directory_manager.set_directories(test_dir)
        self.assertIn(test_dir, self.directory_manager.plugin_directories)
        self.assertNotIn(current_dirs,
                         self.directory_manager.plugin_directories)

    def test_get_dir_iterator_recursive(self):
        recursive_path = path.realpath(path.join(__file__, '..', '..'))
        # alias for pep8
        dir_manager = self.directory_manager
        directories = dir_manager.collect_directories(recursive_path)
        self.assertTrue(len(directories) > 1)

    def test_blacklist_directories(self):
        temp_dir = tempfile.TemporaryDirectory()
        second_temp_dir = tempfile.TemporaryDirectory(dir=temp_dir.name)
        temp_dir_name = temp_dir.name
        second_dir_name = second_temp_dir.name
        self.directory_manager.add_blacklisted_directories(second_dir_name)
        dirs = self.directory_manager.collect_directories(temp_dir_name)
        second_temp_dir.cleanup()
        temp_dir.cleanup()
        self.assertNotIn(second_temp_dir.name, dirs)
        self.assertIn(temp_dir.name, dirs)

    def test_get_dir_iterator_not_recursive(self):
        # default dir is the package dir, which has multiple dirs
        self.directory_manager.recursive = False
        directories = self.directory_manager.get_directories()
        self.assertEqual(len(directories), 1)


if __name__ == '__main__':
    unittest.main()
