import os
import unittest
import tempfile
from simpleyapsy.file_locator import FileLocator


class TestClass:
    pass


class TestFileLocator(unittest.TestCase):
    def setUp(self):
        self.file_locator = FileLocator()

    def test_add_plugin_directory(self):
        test_dir = 'my/plugin/dir'
        self.file_locator.add_plugin_directories(test_dir)
        self.assertIn(test_dir, self.file_locator.plugin_directories)

    def test_set_plugin_directory(self):
        current_dirs = self.file_locator.plugin_directories[0]
        test_dir = 'my/plugin/dir'
        self.file_locator.set_plugin_directories(test_dir)
        self.assertIn(test_dir, self.file_locator.plugin_directories)
        self.assertNotIn(current_dirs, self.file_locator.plugin_directories)

    def test_set_file_getters(self):
        current_file_getters = self.file_locator.file_getters[0]
        # Create a abstract object for testing
        obj = TestClass()
        self.file_locator.set_file_getters(obj)
        self.assertNotIn(current_file_getters, self.file_locator.file_getters)
        self.assertIn(obj, self.file_locator.file_getters)

    def test_add_file_getters(self):
        test_obj = TestClass()
        self.file_locator.add_file_getters(test_obj)
        self.assertIn(test_obj, self.file_locator.file_getters)

    def test_get_dir_iterator_recursive(self):
        dir = os.path.dirname(__file__)
        test_dir = os.path.join(dir, '..')
        walk_iter = self.file_locator._get_dir_iterator(test_dir)
        self.assertNotEqual(len(walk_iter), 1)

    def test_get_dir_iterator_not_recursive(self):
        # assume home dir has dirs
        test_dir = os.path.expanduser('~')
        self.file_locator.recursive = False
        walk_iter = self.file_locator._get_dir_iterator(test_dir)
        self.assertEqual(len(walk_iter), 1)

    def test_plugin_paths_to_absolute(self):
        self.file_locator.set_plugin_directories('simpleyapsy')
        plugin_dirs = self.file_locator.plugin_directories
        self.assertFalse(os.path.isabs(plugin_dirs[0]))
        self.file_locator._plugin_dirs_to_absolute_paths()
        plugin_dirs = self.file_locator.plugin_directories
        self.assertTrue(os.path.isabs(plugin_dirs[0]))


if __name__ == '__main__':
    unittest.main()
