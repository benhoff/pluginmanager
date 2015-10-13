import os
import unittest
from simpleyapsy.module_loader import ModuleLoader


class TestClass:
    pass


class TestModuleLoader(unittest.TestCase):
    def setUp(self):
        self.module_loader = ModuleLoader()

    def test_set_module_parsers(self):
        test_obj = TestClass()
        previous_module = self.module_loader.module_parsers[0]
        self.module_loader.set_module_parsers(test_obj)
        self.assertIn(test_obj, self.module_loader.module_parsers)
        self.assertNotIn(previous_module, self.module_loader.module_parsers)

    def test_add_module_parser(self):
        test_obj = TestClass()
        self.module_loader.add_module_parsers(test_obj)
        self.assertIn(test_obj, self.module_loader.module_parsers)

    def test_blacklist_filepaths(self):
        test_filepath = 'fancy/dir'
        self.module_loader.blacklist_filepaths(test_filepath)
        test_filepaths = ['dir/d', 'dir/b']
        self.module_loader.blacklist_filepaths(test_filepaths)
        self.assertIn(test_filepath, self.module_loader.blacklisted_filepaths)
        self.assertIn(test_filepaths[0],
                      self.module_loader.blacklisted_filepaths)

    def test_set_blacklist_filepaths(self):
        removed_dir = 'test/dir'
        self.module_loader.blacklist_filepaths(removed_dir)
        single_dir = 'dir/b'
        self.module_loader.set_blacklisted_filepaths(single_dir)
        self.assertIn(single_dir, self.module_loader.blacklisted_filepaths)
        mulitple_dirs = ['dir/a', 'dir/b']
        self.module_loader.set_blacklisted_filepaths(mulitple_dirs)
        self.assertIn(mulitple_dirs[0],
                      self.module_loader.blacklisted_filepaths)

    def test_valid_filepath(self):
        blacklist_filepath = 'dir/blacklist'
        processed_filepath = 'dir/processed'
        test_filepath = 'dir/test'
        self.module_loader.blacklist_filepaths(blacklist_filepath)
        self.module_loader.processed_filepaths['test'] = processed_filepath
        # test blacklisted filepath
        valid = self.module_loader._valid_filepath(blacklist_filepath)
        self.assertFalse(valid)
        # test processed_filepath
        valid = self.module_loader._valid_filepath(processed_filepath)
        self.assertFalse(valid)
        # test regular dir
        valid = self.module_loader._valid_filepath(test_filepath)
        self.assertTrue(valid)

    def test_process_filepath(self):
        test_dir = os.path.dirname(__file__)
        expected_filepath = os.path.join(test_dir, '__init__.py')
        processed_file = self.module_loader._process_filepath(test_dir)
        self.assertEqual(expected_filepath, processed_file)
        no_ext = expected_filepath[:-3]
        processed_ext = self.module_loader._process_filepath(no_ext)
        self.assertEqual(processed_ext, expected_filepath)
