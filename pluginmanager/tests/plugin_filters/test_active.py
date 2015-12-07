import unittest

from . import ActiveTestClass

from pluginmanager.plugin_filters import ActiveFilter


class TestActivated(unittest.TestCase):
    def test_activated(self):
        deactivated_test = ActiveTestClass()
        activated_test = ActiveTestClass(True)
        plugins = [deactivated_test, activated_test]
        filter_ = ActiveFilter()

        filtered_plugins = filter_(plugins)
        self.assertIn(activated_test, filtered_plugins)
        self.assertNotIn(deactivated_test, filtered_plugins)

        filter_.active = False

        filtered_plugins = filter_(plugins)
        self.assertNotIn(activated_test, filtered_plugins)
        self.assertIn(deactivated_test, filtered_plugins)
