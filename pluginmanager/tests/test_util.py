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

    def test_get_paths_from_dir(self):
        # TODO: make temp dir, make dir in temp dir and make file
        # in temp dir. see if can get file and dir
        pass

if __name__ == '__main__':
    unittest.main()
