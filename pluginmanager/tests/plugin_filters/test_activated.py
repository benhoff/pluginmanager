import unittest

from . import ActiveTestClass

from simpleyapsy.plugin_filters import activated


class TestActivated(unittest.TestCase):
    def test_activated(self):
        deactivated_test = ActiveTestClass()
        activated_test = ActiveTestClass(True)
        plugins = [deactivated_test, activated_test]
        filtered_plugins = activated(plugins)
        self.assertIn(activated_test, filtered_plugins)
        self.assertNotIn(deactivated_test, filtered_plugins)
