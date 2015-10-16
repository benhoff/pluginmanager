import types
import unittest
from pluginmanager import IPlugin
from pluginmanager.module_parsers import SubclassParser


class Subclass(IPlugin):
    pass


class TestSubclassParser(unittest.TestCase):
    def setUp(self):
        self.parser = SubclassParser()

    def test_get_plugins(self):
        test_module = types.ModuleType("TestModule")
        test_module.IPlugin = IPlugin
        test_module.Subclass = Subclass
        plugins = self.parser.get_plugins(test_module)
        self.assertIn(Subclass, plugins)
        self.assertNotIn(IPlugin, plugins)
