import unittest
from pluginmanager import PluginManager


class InstanceClass(object):
    def __init__(self, active=False):
        self.active = active
        self.name = 'instance_class'
        self.config = {}

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def get_configuration_template(self):
        return {'key_example': None}

    def configure(self, config):
        self.config = config


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
        uniq = self.plugin_manager._unique_class(InstanceClass)
        self.assertFalse(uniq)

    def test_blacklist_plugins(self):
        self.plugin_manager.add_blacklisted_plugins(InstanceClass)
        blacklisted = self.plugin_manager.get_blacklisted_plugins()
        self.assertIn(InstanceClass, blacklisted)

    def test_handle_classs_instance(self):
        self.plugin_manager.instantiate_classes = False
        is_none = self.plugin_manager._handle_class_instance(5)
        self.assertIsNone(is_none)

    def test_class_instance_not_unique(self):
        self.plugin_manager.unique_instances = False
        num_plugins = len(self.plugin_manager.plugins)
        self.plugin_manager._handle_class_instance(InstanceClass)
        self.assertTrue(len(self.plugin_manager.plugins) > num_plugins)

    def test_class_instance_unique(self):
        num_plugins = len(self.plugin_manager.plugins)
        self.plugin_manager.unique_instances = True
        self.plugin_manager._handle_class_instance(InstanceClass)
        self.assertTrue(len(self.plugin_manager.plugins) == num_plugins)

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

    def test_get_config_template(self):
        config = self.plugin_manager.get_configuration_templates()
        self.assertIn('instance_class', config)
    """
    def test_configure_plugins(self):
        config = {'instance_class': {'key_example': 1.0}}
        self.plugin_manager.configure_plugins(config)
    """

    def test_deactive_instances(self):
        instance = InstanceClass(True)
        self.plugin_manager.add_plugins(instance)
        self.plugin_manager.deactivate_plugins()
        instances = self.plugin_manager.get_plugins()
        for instance in instances:
            self.assertFalse(instance.active)
