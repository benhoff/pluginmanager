import unittest
from simpleyapsy import InstanceManager


class InstanceClass(object):
    def __init__(self, active=False):
        self.active = active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class TestInstanceManager(unittest.TestCase):
    def setUp(self):
        self.instance = InstanceClass()
        self.instance_manager = InstanceManager()
        self.instance_manager.add_instances(self.instance)

    def test_add_instances(self):
        self.instance_manager.unique_instances = False
        instance = InstanceClass()
        self.instance_manager.add_instances(instance)
        instances = self.instance_manager.get_instances()
        self.assertIn(instance, instances)
        self.instance_manager.add_instances(InstanceClass())
        instances = self.instance_manager.get_instances()
        self.assertTrue(len(instances) > 2)

    def test_set_instances(self):
        instance_2 = InstanceClass()
        self.instance_manager.set_instances(instance_2)
        instances = self.instance_manager.get_instances()
        self.assertIn(instance_2, instances)
        self.assertNotIn(self.instance, instances)

    def test_activate_instances(self):
        self.instance_manager.activate_instances()
        instances = self.instance_manager.get_instances()
        self.assertTrue(instances[0].active)

    def test_deactive_instances(self):
        instance = InstanceClass(True)
        self.instance_manager.add_instances(instance)
        self.instance_manager.deactivate_instances()
        instances = self.instance_manager.get_instances()
        for instance in instances:
            self.assertFalse(instance.active)
