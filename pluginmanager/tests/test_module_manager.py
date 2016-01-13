import os
import sys
import types
import logging
import unittest
from .compat import tempfile
from pluginmanager.module_manager import ModuleManager


class TestModuleManager(unittest.TestCase):
    def setUp(self):
        """
        create the module manager and a temporary directory.
        Write a python file with several data members into
        the created temporary directory.
        """
        self.module_manager = ModuleManager()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.code_filepath = os.path.join(self.temp_dir.name, "mod_test.py")
        code = 'PLUGINS = [5,4]\nfive = 5.0\ndef func():\n\tpass'
        with open(self.code_filepath, 'w+') as f:
            f.write(code)

    def tearDown(self):
        """
        cleanup the temporary directory created in the setUp method.
        """
        self.temp_dir.cleanup()

    def test_load_modules(self):
        """
        Create some test code. write it into the test code filepath.
        Then load the test code. Assert that the test code has all
        the desired attributes. Assert that the filepath is in the processed
        filepaths and that the expected module name is in the processed
        filepaths and the loaded modules.
        """
        module = self.module_manager.load_modules(self.code_filepath).pop()
        self.assertTrue(hasattr(module, 'PLUGINS'))
        self.assertTrue(hasattr(module, 'func'))
        self.assertTrue(hasattr(module, 'five'))
        self.assertEqual(module.PLUGINS, [5, 4])
        self.assertEqual(module.five, 5.0)
        del sys.modules[module.__name__]
        del module
        expected_module_name = 'pluginmanager_plugin_mod_test_0'
        self.assertIn(expected_module_name, self.module_manager.loaded_modules)
        self.assertIn(self.code_filepath,
                      self.module_manager.processed_filepaths.values())

        self.assertIn(expected_module_name,
                      self.module_manager.processed_filepaths.keys())

    def test_load_modules_with_processed_filepath(self):
        """
        add a filepath to the processed filepaths and then assert that
        the loaded modules are empty.
        """
        self.module_manager.processed_filepaths['test'] = self.code_filepath
        modules = self.module_manager.load_modules(self.code_filepath)
        self.assertEqual(len(modules), 0)

    def test_collect_plugins(self):
        """
        Create a module with a data member `blue`
        collect the plugins from the module and assert that the data member
        is present in the collected plugins. Next, collect the plugins without
        passing in an argument and assert it's empty. Lastly, add the module to
        the loaded modules and collect plugins without passing in anything
        explicitly into the method call. Assert that blue is still present in
        the collected modules.
        """
        module_name = 'test_pluginmanager_module'
        module = types.ModuleType(module_name)
        blue = 'blue data member'
        module.blue = blue
        plugins = self.module_manager.collect_plugins(module)
        self.assertIn(blue, plugins)

        empty_plugins = self.module_manager.collect_plugins()
        self.assertEqual(len(empty_plugins), 0)

        self.module_manager.add_to_loaded_modules(module)
        sys.modules[module_name] = module
        loaded_module_plugins = self.module_manager.collect_plugins()
        self.assertIn(blue, loaded_module_plugins)
        del sys.modules[module_name]

    def test_set_module_plugin_filters(self):
        """
        create and add some state in the module filters. Then set the module
        filters with a test object. assert that the test object is in the
        module filters and that the previous state is not.
        """
        previous_module = object()
        self.module_manager.add_module_plugin_filters(previous_module)
        test_obj = object()
        self.module_manager.set_module_plugin_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_plugin_filters)
        self.assertNotIn(previous_module,
                         self.module_manager.module_plugin_filters)

    def test_add_to_loaded_modules(self):
        """
        assert that the module `types` is not being tracked. Then add the
        actual module to the loaded modules and assert that the string name
        is there.
        Also want to test the string handeling, so pass in a test string and
        assert that it is in tracked.
        """
        types_module_str = 'types'
        self.assertNotIn(types_module_str, self.module_manager.loaded_modules)
        self.module_manager.add_to_loaded_modules(types)
        self.assertIn(types_module_str, self.module_manager.loaded_modules)

        test_module_name = 'bogus'
        self.assertNotIn(test_module_name, self.module_manager.loaded_modules)
        self.module_manager.add_to_loaded_modules(test_module_name)
        self.assertIn(test_module_name, self.module_manager.loaded_modules)

    def test_get_loaded_modules(self):
        """
        get out the loaded modules. Assert that it is a list and is
        empty. Assert that the module `types` is not present. Then add
        the module `types` to tracked internally. get the loaded modules
        again and assert that the module `types` is present.
        """
        default_modules = self.module_manager.get_loaded_modules()
        self.assertTrue(isinstance(default_modules, list))
        self.assertEqual(len(default_modules), 0)

        self.assertNotIn(types, default_modules)
        self.module_manager.add_to_loaded_modules(types)
        gotten_modules = self.module_manager.get_loaded_modules()
        self.assertIn(types, gotten_modules)

    def test_add_module_plugin_filter(self):
        """
        add a test object to the module filters and assert that it is in there.
        """
        test_obj = object()
        self.module_manager.add_module_plugin_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_plugin_filters)

    def test_get_module_plugin_filters(self):
        """
        Assert that the module plugin filters are empty at first. Add an
        object. Use the method to get all of the plugin filters out. Assert
        that the object returned from the method is a set. That it only has
        one object, and that the one object was the object added.
        """
        self.assertEqual(len(self.module_manager.get_module_plugin_filters()),
                         0)

        test_obj = object()
        self.module_manager.add_module_plugin_filters(test_obj)
        gotten_filters = self.module_manager.get_module_plugin_filters()
        self.assertTrue(isinstance(gotten_filters, list))
        self.assertEqual(len(gotten_filters), 1)
        self.assertIn(test_obj, gotten_filters)

    def test_remove_module_plugin_filters(self):
        """
        create an object, add it to the module plugin filters. Assert that the
        object is there. call the method to remove the object. Assert that it
        is not there.
        """
        test_obj = object()
        self.module_manager.add_module_plugin_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_plugin_filters)
        self.module_manager.remove_module_plugin_filters(test_obj)
        self.assertNotIn(test_obj, self.module_manager.module_plugin_filters)

    def test_load_failing_module(self):
        """
        This tests that a failing import does not stop the program
        Currently, logging is disabled to prevent noise in the logs.
        Should change it to expect the log. Should.
        """
        logging.disable(logging.CRITICAL)
        filepath = os.path.join(self.temp_dir.name, 'fail.py')
        with open(filepath, 'w+') as f:
            f.write('blue=5/nred=')
        self.module_manager.load_modules(filepath)
        logging.disable(logging.NOTSET)

    def test_filter_modules(self):
        """
        Create a filter that returns only instances of floats. Create a list
        of plugins that include both a float and a non-float member.
        pass the list through the filter function and assert that the float
        member made it, while the non float member did not.
        """
        def filter_(plugins, *args):
            result = []
            for plugin in plugins:
                if isinstance(plugin, float):
                    result.append(plugin)
            return result
        self.module_manager.add_module_plugin_filters(filter_)
        instance = object()
        plugins = [5.0, instance]
        filtered = self.module_manager._filter_modules(plugins, [])
        self.assertNotIn(instance, filtered)
        self.assertIn(5.0, filtered)

        def bad_filter(plugins, *args):
            for plugin in plugins:
                if not isinstance(plugin, float):
                    plugins.remove(plugin)
            return plugins

        self.module_manager.set_module_plugin_filters(bad_filter)
        self.module_manager._filter_modules(plugins, [])

    def test_processed_filepath(self):
        """
        Create two fake filepaths, a "processed" filepath and an
        unprocessed filepath. Set the processed filepath in the internal
        data memeber `processed_filepaths`. Then test the prescribed method,
        asserting that the processed filepath returns a True, while the
        unprocessed filepath correctly returns a False
        """
        processed_filepath = 'dir/processed'
        test_filepath = 'dir/test'
        self.module_manager.processed_filepaths['test'] = processed_filepath
        # test processed_filepath
        processed = self.module_manager._processed_filepath(processed_filepath)
        self.assertTrue(processed)
        # test regular dir
        unprocessed = self.module_manager._processed_filepath(test_filepath)
        self.assertFalse(unprocessed)

    def test_clean_filepath(self):
        """
        Create an `__init__.py` file in the temp dir. Pass the temp dir
        filepath into the prescribed method and assert that the returned
        filepath is the created `__init__.py` file in the temp dir.

        Next, pull off the extension information from the file and repass the
        filepath in, asserting that it correctly reappends the expected
        extension.
        """
        expected_filepath = os.path.join(self.temp_dir.name, '__init__.py')
        open(expected_filepath, 'a+').close()
        cleaned_file = self.module_manager._clean_filepath(self.temp_dir.name)
        self.assertEqual(cleaned_file, expected_filepath)
        no_ext = expected_filepath[:-3]
        processed_ext = self.module_manager._clean_filepath(no_ext)
        self.assertEqual(processed_ext, expected_filepath)

    def test_update_loaded_modules(self):
        """
        Add the filepath created in setup to the processed filepath with the
        name `module_name`. Also add the `module_name` to sys.modules
        """
        module_name = 'test_pluginmanager'
        self.module_manager.loaded_modules.add(module_name)
        processed_filepaths = self.module_manager.processed_filepaths
        processed_filepaths[module_name] = self.code_filepath
        sys.modules[module_name] = None
        self.module_manager._update_loaded_modules()
        self.assertIn(module_name, self.module_manager.loaded_modules)
        self.assertIn(module_name, processed_filepaths.keys())
        del sys.modules[module_name]
        self.module_manager._update_loaded_modules()
        self.assertNotIn(module_name, processed_filepaths.keys())
        self.assertNotIn(module_name, self.module_manager.loaded_modules)
