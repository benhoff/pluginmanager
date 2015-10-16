import unittest
from . import ActiveTestClass
from pluginmanager.plugin_filters import deactivated


class TestDeactivated(unittest.TestCase):
    def test_deactivated(self):
        deactivated_test = ActiveTestClass()
        activated_test = ActiveTestClass(True)
        plugins = [deactivated_test, activated_test]
        filtered_plugins = deactivated(plugins)
        self.assertNotIn(activated_test, filtered_plugins)
        self.assertIn(deactivated_test, filtered_plugins)
