import os
import types
import unittest
import tempfile
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
            f.write('       super().__init__()')
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

    def test_set_plugins(self):
        self.interface.set_plugins(self.test_obj)
        plugins = self.interface.get_plugins()
        self.assertIn(self.test_obj, plugins)
