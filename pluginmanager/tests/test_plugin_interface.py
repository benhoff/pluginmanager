import os
import sys
import types
import unittest
from .compat import tempfile
from pluginmanager.plugin_interface import PluginInterface
from pluginmanager.iplugin import IPlugin


class TestInterface(unittest.TestCase):
    def setUp(self):
        self.test_obj = IPlugin()
        self.interface = PluginInterface()

        # fixes weird state issues on my machine
        self.interface.file_manager.set_file_filters([])
        self.interface.module_manager.set_module_filters([])

    def test_collect_plugins_no_args(self):
        temp_dir = tempfile.TemporaryDirectory()
        with open(os.path.join(temp_dir.name, 'a.py'), 'w+') as f:
            f.write('import pluginmanager\n')
            f.write('class T(pluginmanager.IPlugin):\n')
            f.write("    name='red'\n")
            f.write('    def __init__(self):\n')
            f.write('       super(T, self).__init__()')
        self.interface.set_plugin_directories(temp_dir.name)
        plugin = self.interface.collect_plugins()[0]
        temp_dir.cleanup()
        self.assertEqual(plugin.name, 'red')

    def test_collect_plugin_directories(self):
        dir_names = []
        dirs = []
        with tempfile.TemporaryDirectory() as main_dir:
            self.interface.set_plugin_directories(main_dir)
            dir_names.append(main_dir)
            with tempfile.TemporaryDirectory(dir=main_dir) as recursive_dir:
                dir_names.append(recursive_dir)
                dirs = self.interface.collect_plugin_directories(main_dir)
        self.assertIn(dir_names[0], dirs)
        self.assertIn(dir_names[1], dirs)

    def test_collect_plugin_filepaths(self):
        filename = 'test.py'
        filepaths = []
        with tempfile.TemporaryDirectory() as main_dir:
            filename = os.path.join(main_dir, filename)
            open(filename, 'a+').close()
            filepaths = self.interface.collect_plugin_filepaths(main_dir)
        self.assertIn(filename, filepaths)

    def test_load_modules(self):
        module = None
        with tempfile.NamedTemporaryFile(suffix='.py') as file:
            file.write(b'test=1')
            file.seek(0)
            module = self.interface.load_modules(file.name)
        module = module.pop()
        self.assertEqual(module.test, 1)

    def test_collect_plugins(self):
        module = types.ModuleType('test')
        module.test = 5
        plugins = self.interface.collect_plugins(module)
        self.assertIn(5, plugins)

    def test_track_site_package_path(self):
        # TODO: better test method
        num_directories = len(self.interface.get_plugin_directories())
        self.interface.track_site_package_paths()
        new_num_dirs = len(self.interface.get_plugin_directories())
        self.assertTrue(new_num_dirs > num_directories)

    def test_plugins(self):
        plugin_1 = IPlugin()
        plugin_2 = IPlugin()
        self.interface.add_plugins([plugin_1])
        plugins = self.interface.get_plugins()
        self.assertIn(plugin_1, plugins)
        self.interface.set_plugins(plugin_2)
        set_plugins = self.interface.get_plugins()
        self.assertIn(plugin_2, set_plugins)
        self.assertNotIn(plugin_1, set_plugins)
        self.interface.remove_plugins(plugin_2)
        removed_plugins = self.interface.get_plugins()
        self.assertNotIn(plugin_2, removed_plugins)

    def test_add_plugin_filepaths(self):
        filepath_1 = '/tmp/a.py'
        filepath_2 = '/tmp/b.py'
        self.interface.add_plugin_filepaths(filepath_1)
        filepaths = self.interface.get_plugin_filepaths()
        self.assertIn(filepath_1, filepaths)
        self.interface.set_plugin_filepaths(filepath_2)
        set_filepaths = self.interface.get_plugin_filepaths()
        self.assertIn(filepath_2, set_filepaths)
        self.assertNotIn(filepath_1, set_filepaths)
        self.interface.remove_plugin_filepaths(filepath_2)
        removed_filepaths = self.interface.get_plugin_filepaths()
        self.assertNotIn(filepath_2, removed_filepaths)

    def test_add_get_set_dirs(self):
        dir_1 = '/tmp/dir'
        dir_2 = '/tmp/dir_2'
        self.interface.add_plugin_directories(dir_1)
        dirs = self.interface.get_plugin_directories()
        self.assertIn(dir_1, dirs)
        self.interface.set_plugin_directories(dir_2)
        set_dirs = self.interface.get_plugin_directories()
        self.assertIn(dir_2, set_dirs)
        self.assertNotIn(dir_1, set_dirs)
        self.interface.remove_plugin_directories(dir_2)
        removed_dirs = self.interface.get_plugin_directories()
        self.assertNotIn(dir_2, removed_dirs)

    def test_set_plugins(self):
        self.interface.set_plugins(self.test_obj)
        plugins = self.interface.get_plugins()
        self.assertIn(self.test_obj, plugins)

    def test_add_get_modules(self):
        module_name = 'test_module_type'
        test_module = types.ModuleType(module_name)
        sys.modules[module_name] = test_module
        self.interface.add_to_loaded_modules(test_module)
        loaded_modules = self.interface.get_loaded_modules()
        self.assertIn(test_module, loaded_modules)

    def test_interface(self):
        template = '{}_blacklisted_{}'
        methods = ['filepaths', 'plugins']
        get_func = lambda attr: getattr(self.interface, attr)

        adders = [get_func(template.format('add',
                                           method)) for method in methods]

        setters = [get_func(template.format('set',
                                            method)) for method in methods]

        getters = [get_func(template.format('get',
                                            method)) for method in methods]

        removers = [get_func(template.format('remove',
                                             method)) for method in methods]
        instance = object()
        second_instance = object()
        for adder, setter, getter, remover in zip(adders, setters,
                                                  getters, removers):

            adder(instance)
            self.assertIn(instance, getter())
            setter(second_instance)
            self.assertIn(second_instance, getter())
            self.assertNotIn(instance, getter())
            remover(second_instance)
            self.assertNotIn(second_instance, getter())
    """
    def test_add_plugin_directories(self):
        added_dir = 'pluginmanager'
        self.interface.add_plugin_directories(added_dir)
        directories = self.interface.get_plugin_directories()
        self.assertIn(added_dir, directories)

    def test_set_plugin_directories(self):
        preset_dir = self.interface.get_plugin_directories().pop()
        set_dir = 'pluginmanager'
        self.interface.set_plugin_directories(set_dir)
        directories = self.interface.get_plugin_directories()
        self.assertIn(set_dir, directories)
        self.assertNotIn(preset_dir, directories)
    """

    def test_set_blacklist_filepath(self):
        filepath = 'test/dir'
        self.interface.set_blacklisted_filepaths(filepath)
        blacklisted = self.interface.get_blacklisted_filepaths()
        self.assertIn(filepath, blacklisted)

    def test_test_interface(self):
        # all methods in interface follow this pattern
        template = '{}_{}_filters'
        # currently the only two filters supported are file and module
        filters = ['file', 'module']
        # set up a function to get the actual method calls
        get_func = lambda attr: getattr(self.interface, attr)
        # list comprhensions, our function, and filters to get all the methods
        adders = [get_func(template.format('add',
                                           filter_)) for filter_ in filters]

        setters = [get_func(template.format('set',
                                            filter_)) for filter_ in filters]

        getters = [get_func(template.format('get',
                                            filter_)) for filter_ in filters]

        removers = [get_func(template.format('remove',
                                             filter_)) for filter_ in filters]
        instance = object()
        second_instance = object()
        for adder, setter, getter, remover in zip(adders, setters,
                                                  getters, removers):

            adder(instance)
            self.assertIn(instance, getter())
            setter(second_instance)
            self.assertIn(second_instance, getter())
            self.assertNotIn(instance, getter())
            remover(second_instance)
            self.assertNotIn(second_instance, getter())
