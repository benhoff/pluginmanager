import os
import unittest
from simpleyapsy.directory_manager import DirectoryManager


class TestDirectoryManager(unittest.TestCase):
    def setUp(self):
        self.directory_manager = DirectoryManager()

    def test_add_plugin_directory(self):
        test_dir = 'my/plugin/dir'
        self.directory_manager.add_directories(test_dir)
        self.assertIn(test_dir, self.directory_manager.plugin_directories)

    def test_set_plugin_directory(self):
        current_dirs = self.directory_manager.plugin_directories.pop()
        test_dir = 'my/plugin/dir'
        self.directory_manager.set_directories(test_dir)
        self.assertIn(test_dir, self.directory_manager.plugin_directories)
        self.assertNotIn(current_dirs,
                         self.directory_manager.plugin_directories)

    def test_get_dir_iterator_recursive(self):
        directories = self.directory_manager.get_directories()
        self.assertTrue(len(directories) > 1)

    def test_get_dir_iterator_not_recursive(self):
        # default dir is the package dir, which has multiple dirs
        self.directory_manager.recursive = False
        directories = self.directory_manager.get_directories()
        self.assertEqual(len(directories), 1)

    def test_plugin_paths_to_absolute(self):
        self.directory_manager.set_directories('simpleyapsy')
        plugin_dirs = self.directory_manager.plugin_directories
        self.assertFalse(os.path.isabs(next(iter(plugin_dirs))))
        self.directory_manager._plugin_dirs_to_absolute_paths()
        plugin_dirs = self.directory_manager.plugin_directories
        self.assertTrue(os.path.isabs(plugin_dirs.pop()))

if __name__ == '__main__':
    unittest.main()
