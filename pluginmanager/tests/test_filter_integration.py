import os
import types
import unittest
from .compat import tempfile
import pluginmanager


class TestClass(pluginmanager.IPlugin):
    def __init__(self):
        super(TestClass, self).__init__()


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.interface = pluginmanager.PluginInterface()

    def test_file_filters(self):
        bogus_file = str()
        init = str()
        blue_file = str()
        contains_init = []
        contains_blue = []
        temp_dir = tempfile.TemporaryDirectory()
        dir_name = temp_dir.name
        filename_filter = pluginmanager.file_filters.FilenameFileFilter()
        self.interface.set_file_filters(filename_filter)
        init = os.path.join(dir_name, '__init__.py')
        bogus_file = os.path.join(dir_name, 'bogus.py')
        blue_file = os.path.join(dir_name, 'blue.py')
        open(init, 'a+').close()
        open(bogus_file, 'a+').close()
        open(blue_file, 'a+').close()
        contains_init = self.interface.collect_plugin_filepaths(dir_name)
        regex = pluginmanager.file_filters.MatchingRegexFileFilter('blue.py')
        self.interface.set_file_filters(regex)
        contains_blue = self.interface.collect_plugin_filepaths(dir_name)
        temp_dir.cleanup()
        self.assertIn(init, contains_init)
        self.assertIn(blue_file, contains_blue)
        self.assertNotIn(bogus_file, contains_init)
        self.assertNotIn(bogus_file, contains_blue)

    def test_module_filters(self):
        module = types.ModuleType('test')
        module.plugin = pluginmanager.IPlugin
        module.test_plugin = TestClass
        bogus = 'five'
        module.bogus = bogus
        subclass_parser = pluginmanager.module_filters.SubclassParser()
        self.interface.set_module_filters(subclass_parser)
        contains_plugin = self.interface.collect_plugins(module)
        self.assertIn(TestClass, contains_plugin)
        self.assertNotIn(bogus, contains_plugin)
