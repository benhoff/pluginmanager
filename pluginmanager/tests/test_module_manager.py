import os
import unittest
from pluginmanager.module_manager import ModuleManager


class TestClass:
    pass


class TestModuleManager(unittest.TestCase):
    def setUp(self):
        self.module_manager = ModuleManager()

    def test_set_module_filters(self):
        test_obj = TestClass()
        previous_module = self.module_manager.module_filters[0]
        self.module_manager.set_module_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_filters)
        self.assertNotIn(previous_module, self.module_manager.module_filters)

    def test_add_module_parser(self):
        test_obj = TestClass()
        self.module_manager.add_module_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_filters)

    def test_add_blacklisted_filepaths(self):
        test_filepath = 'fancy/dir'
        self.module_manager.add_blacklisted_filepaths(test_filepath)
        test_filepaths = ['dir/d', 'dir/b']
        self.module_manager.add_blacklisted_filepaths(test_filepaths)
        self.assertIn(test_filepath, self.module_manager.blacklisted_filepaths)
        self.assertIn(test_filepaths[0],
                      self.module_manager.blacklisted_filepaths)

    def test_set_blacklist_filepaths(self):
        removed_dir = 'test/dir'
        self.module_manager.add_blacklisted_filepaths(removed_dir)
        single_dir = 'dir/b'
        self.module_manager.set_blacklisted_filepaths(single_dir)
        self.assertIn(single_dir, self.module_manager.blacklisted_filepaths)
        mulitple_dirs = ['dir/a', 'dir/b']
        self.module_manager.set_blacklisted_filepaths(mulitple_dirs)
        self.assertIn(mulitple_dirs[0],
                      self.module_manager.blacklisted_filepaths)

    def test_valid_filepath(self):
        blacklist_filepath = 'dir/blacklist'
        processed_filepath = 'dir/processed'
        test_filepath = 'dir/test'
        self.module_manager.add_blacklisted_filepaths(blacklist_filepath)
        self.module_manager.processed_filepaths['test'] = processed_filepath
        # test blacklisted filepath
        valid = self.module_manager._valid_filepath(blacklist_filepath)
        self.assertFalse(valid)
        # test processed_filepath
        valid = self.module_manager._valid_filepath(processed_filepath)
        self.assertFalse(valid)
        # test regular dir
        valid = self.module_manager._valid_filepath(test_filepath)
        self.assertTrue(valid)

    def test_process_filepath(self):
        test_dir = os.path.dirname(__file__)
        expected_filepath = os.path.join(test_dir, '__init__.py')
        processed_file = self.module_manager._process_filepath(test_dir)
        self.assertEqual(expected_filepath, processed_file)
        no_ext = expected_filepath[:-3]
        processed_ext = self.module_manager._process_filepath(no_ext)
        self.assertEqual(processed_ext, expected_filepath)
