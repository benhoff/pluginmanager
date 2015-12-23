import sys
import unittest
from pluginmanager import util


class TestUtil(unittest.TestCase):
    def test_get_module_name(self):
        ends_with_init = 'my/dirname/__init__.py'
        python_file = 'my/path/test.py'
        ends_with_init = util.get_module_name(ends_with_init)
        python_file = util.get_module_name(python_file)
        self.assertEqual(ends_with_init, 'dirname')
        self.assertEqual(python_file, 'test')

    def test_create_unique_module_name(self):
        name = 'test'
        module_name = util.create_unique_module_name(name)
        sys.modules[module_name] = None
        second_module_name = util.create_unique_module_name(name)
        self.assertNotEqual(module_name, second_module_name)
        self.assertEqual(module_name, 'pluginmanager_plugin_test_0')
        self.assertEqual(second_module_name, 'pluginmanager_plugin_test_1')

    def test_create_module_name_with_dict(self):
        name = {'name': 'test'}
        name = util.create_unique_module_name(name)
        self.assertEqual(name, 'pluginmanager_plugin_test_0')

    def test_remove_from_set(self):
        obj_1 = object()
        obj_2 = object()
        test_set = set((obj_1, obj_2))
        remove_set = set((obj_2,))

        result_set = util.remove_from_set(test_set, remove_set)
        self.assertIn(obj_1, result_set)
        self.assertNotIn(obj_2, result_set)

    def test_remove_from_list(self):
        obj_1 = object()
        obj_2 = object()
        test_set = [obj_1, obj_2]
        remove_set = [obj_2, ]

        result_set = util.remove_from_list(test_set, remove_set)
        self.assertIn(obj_1, result_set)
        self.assertNotIn(obj_2, result_set)


if __name__ == '__main__':
    unittest.main()
