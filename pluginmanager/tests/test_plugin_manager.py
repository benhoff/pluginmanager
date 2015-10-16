import unittest
from pluginmanager import PluginManager


class InstanceClass(object):
    def __init__(self, active=False):
        self.active = active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class TestPluginManager(unittest.TestCase):
    def setUp(self):
        self.instance = InstanceClass()
        self.plugin_manager = PluginManager()
        self.plugin_manager.add_plugins(self.instance)

    def test_add_instances(self):
        self.plugin_manager.unique_instances = False
        instance = InstanceClass()
        self.plugin_manager.add_plugins(instance)
        instances = self.plugin_manager.get_plugins()
        self.assertIn(instance, instances)
        self.plugin_manager.add_plugins(InstanceClass())
        instances = self.plugin_manager.get_plugins()
        self.assertTrue(len(instances) > 2)

    def test_set_instances(self):
        instance_2 = InstanceClass()
        self.plugin_manager.set_plugins(instance_2)
        instances = self.plugin_manager.get_plugins()
        self.assertIn(instance_2, instances)
        self.assertNotIn(self.instance, instances)

    def test_activate_instances(self):
        self.plugin_manager.activate_plugins()
        instances = self.plugin_manager.get_plugins()
        self.assertTrue(instances[0].active)

    def test_deactive_instances(self):
        instance = InstanceClass(True)
        self.plugin_manager.add_plugins(instance)
        self.plugin_manager.deactivate_plugins()
        instances = self.plugin_manager.get_plugins()
        for instance in instances:
            self.assertFalse(instance.active)
