import os
import types
import unittest
import tempfile
import pluginmanager


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.interface = pluginmanager.PluginInterface()
        self.filter_interface = self.interface.get_filter_interface()

    def test_file_filters(self):
        bogus_file = str()
        init = str()
        blue_file = str()
        contains_init = []
        contains_blue = []
        with tempfile.TemporaryDirectory() as temp_dir:
            self.filter_interface.set_file_filters(pluginmanager.file_filters.FilenameFileFilter())
            init= os.path.join(temp_dir, '__init__.py')
            bogus_file = os.path.join(temp_dir, 'bogus.py')
            blue_file = os.path.join(temp_dir, 'blue.py')
            open(init, 'a+').close()
            open(bogus_file, 'a+').close()
            open(blue_file, 'a+').close()
            contains_init = self.interface.collect_plugin_filepaths(temp_dir)
            regex = pluginmanager.file_filters.MatchingRegexFileFilter('blue.py')
            self.filter_interface.set_file_filters(regex)
            contains_blue = self.interface.collect_plugin_filepaths(temp_dir)
        self.assertIn(init, contains_init)
        self.assertIn(blue_file, contains_blue)
        self.assertNotIn(bogus_file, contains_init)
        self.assertNotIn(bogus_file, contains_blue)

    def test_module_filters(self):
        module = types.ModuleType('test')
        plugin = pluginmanager.IPlugin()
        module.plugin = plugin
        bogus = 'five'
        module.bogus = bogus
        self.filter_interface.set_module_filters(pluginmanager.module_filters.SubclassParser())
        cotains_plugin = self.interface.collect_plugins(module)
        self.assertIn(plugin, contains_plugin)
        self.assertNotIn(bougs, contains_plugin)

