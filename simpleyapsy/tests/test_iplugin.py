import unittest
from simpleyapsy import IPlugin


class TestObj:
    pass


class TestIPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = IPlugin()

    def test_active(self):
        self.assertFalse(self.plugin.active)

    def test_key_not_in_config(self):
        self.plugin.CONFIG_TEMPLATE = {'api_key': None}
        self.assertRaises(Exception, self.plugin.check_configuration, {})

    def test_autoname(self):
        plugin = IPlugin()
        self.assertEqual(plugin.name, "IPlugin")

    def test_activate(self):
        self.plugin.activate()
        self.assertTrue(self.plugin.active)

    def test_deactivate(self):
        self.plugin.deactivate()
        self.assertFalse(self.plugin.active)

    def test_check_configuration(self):
        self.assertTrue(self.plugin.check_configuration({}))

    def test_configure(self):
        test_obj = TestObj()
        self.plugin.configure(test_obj)
        self.assertEqual(self.plugin.config, test_obj)

    def test_name(self):
        self.assertEqual(self.plugin.name, 'IPlugin')

if __name__ == '__main__':
    unittest.main()
