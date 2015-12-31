import os
import sys
import logging
import unittest
from .compat import tempfile
from pluginmanager.module_manager import ModuleManager


class TestModuleManager(unittest.TestCase):
    def setUp(self):
        self.module_manager = ModuleManager()

    def test_set_module_filters(self):
        previous_module = object()
        self.module_manager.add_module_filters(previous_module)
        test_obj = object()
        self.module_manager.set_module_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_filters)
        self.assertNotIn(previous_module, self.module_manager.module_filters)

    def test_add_module_filter(self):
        test_obj = object()
        self.module_manager.add_module_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_filters)

    def test_failing_module(self):
        """
        This tests that a failing import does not stop the program
        Currently, logging is disabled to prevent noise in the logs.
        Should change it to expect the log. Should.
        """
        logging.disable(logging.CRITICAL)
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = os.path.join(temp_dir, 'fail.py')
            with open(filepath, 'w+') as f:
                f.write('blue=5/nred=')
            self.module_manager.load_modules(filepath)
        logging.disable(logging.NOTSET)

    def test_filter_modules(self):
        def filter_(plugins, *args):
            for plugin in plugins:
                if not isinstance(plugin, float):
                    plugins.remove(plugin)
            return plugins
        self.module_manager.set_module_filters(filter_)
        instance = object()
        plugins = [5.0, instance]
        filtered = self.module_manager._filter_modules(plugins, [])
        self.assertNotIn(instance, filtered)
        self.assertIn(5.0, filtered)

    def test_valid_filepath(self):
        processed_filepath = 'dir/processed'
        test_filepath = 'dir/test'
        self.module_manager.processed_filepaths['test'] = processed_filepath
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

    def _load_modules(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            code = 'PLUGINS = [5,4]\nfive = 5.0\ndef func():\n    pass'
            filename = os.path.join(temp_dir, "mod_test.py")
            f = open(filename, 'w+')
            f.write(code)
            f.close()
            module = self.module_manager.load_modules(filename)
            module = module.pop()
        return module, filename

    def test_get_modules(self):
        module, _ = self._load_modules()
        name = module.__name__
        name = [name]
        got_modules = self.module_manager._get_modules(name)
        self.assertIn(module, got_modules)
        loaded_modules = self.module_manager.get_loaded_modules()
        self.assertIn(module, loaded_modules)

    def test_collect_plugins(self):
        self.module_manager.module_filters = []
        module, _ = self._load_modules()
        plugins = self.module_manager.collect_plugins(module)
        self.assertIn(5.0, plugins)

    def test_load_modules(self):
        module, filename = self._load_modules()

        self.assertIn(filename,
                      self.module_manager.processed_filepaths.values())

        self.assertEqual(module.PLUGINS, [5, 4])
        self.assertEqual(module.five, 5.0)

    def test_update_loaded_modules(self):
        module, filename = self._load_modules()
        module_name = module.__name__
        processed_fps = self.module_manager.processed_filepaths
        self.assertIn(module_name, processed_fps.keys())
        del module
        del sys.modules[module_name]
        self.module_manager._update_loaded_modules()
        self.assertNotIn(module_name, processed_fps.keys())
