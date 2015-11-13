import unittest
from pluginmanager import IPlugin
from pluginmanager.module_filters import SubclassParser


class Subclass(IPlugin):
    pass


class TestSubclassParser(unittest.TestCase):
    def setUp(self):
        self.parser = SubclassParser()

    def test_get_plugins(self):
        plugins = [IPlugin(), 4, IPlugin, Subclass]
        plugins = self.parser(plugins)
        self.assertIn(Subclass, plugins)
        self.assertNotIn(4, plugins)
