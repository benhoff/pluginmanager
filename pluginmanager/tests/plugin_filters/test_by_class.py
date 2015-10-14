import unittest
from . import ActiveTestClass
from pluginmanager.plugin_filters import by_class


class BogusClass:
    pass


class TestByClass(unittest.TestCase):
    def test_by_class(self):
        result = ActiveTestClass()
        to_filter = BogusClass()
        plugins = [result, to_filter]
        plugins = by_class(plugins, ActiveTestClass)
        self.assertIn(result, plugins)
        self.assertNotIn(to_filter, plugins)
