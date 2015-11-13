import unittest
from pluginmanager import PluginManager, IPlugin


class InstanceClass(IPlugin):
    def __init__(self, active=False):
        super(InstanceClass, self).__init__()


def _test_filter(plugins):
    result = []
    for plugin in plugins:
        if hasattr(plugin, 'name') and plugin.name == 'red':
            result.append(plugin)
    return result


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

    def test_register_class(self):
        class TestClass:
            pass

        self.assertFalse(issubclass(TestClass, IPlugin))
        self.plugin_manager.register_classes(TestClass)
        self.assertTrue(issubclass(TestClass, IPlugin))

    def test_class_in_blacklist(self):
        self.plugin_manager.set_plugins([])
        self.plugin_manager.add_blacklisted_plugins(InstanceClass)
        self.plugin_manager._handle_object_instance(self.instance)
        plugins = self.plugin_manager.get_plugins()
        self.assertEqual(plugins, [])

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

    def test_get_plugins(self):
        self.plugin_manager.unique_instances = False
        instance_2 = InstanceClass()
        instance_2.name = 'red'
        self.plugin_manager.add_plugins(instance_2)

        filtered_plugins = self.plugin_manager.get_plugins(_test_filter)
        self.assertNotIn(self.instance, filtered_plugins)
        self.assertIn(instance_2, filtered_plugins)

    def test_set_plugins(self):
        instance_2 = InstanceClass()
        self.plugin_manager.set_plugins(instance_2)
        plugins = self.plugin_manager.get_plugins()
        self.assertIn(instance_2, plugins)
        self.assertNotIn(self.instance, plugins)

    def test_remove_plugin(self):
        self.plugin_manager.remove_plugins(self.instance)
        plugins = self.plugin_manager.get_plugins()
        self.assertNotIn(self.instance, plugins)

    def test_get_instances(self):
        self.plugin_manager.unique_instances = False
        instance_2 = InstanceClass()
        instance_2.name = 'red'
        self.plugin_manager.add_plugins((instance_2, 5.0))
        instances = self.plugin_manager.get_instances((IPlugin, InstanceClass))
        self.assertIn(instance_2, instances)
        self.assertIn(self.instance, instances)
        self.assertNotIn(5.0, instances)
        filtered_instances = self.plugin_manager.get_instances(_test_filter)
        self.assertIn(instance_2, filtered_instances)
        self.assertNotIn(self.instance, filtered_instances)
        self.assertNotIn(5.0, filtered_instances)
        all_instances = self.plugin_manager.get_instances(None)
        self.assertIn(self.instance, all_instances)
        self.assertIn(instance_2, all_instances)
        self.assertIn(5.0, all_instances)

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
