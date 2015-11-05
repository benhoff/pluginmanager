import unittest
from pluginmanager import PluginInterface


class TestObj:
    pass


class TestBlacklistInterface(unittest.TestCase):
    def setUp(self):
        interface = PluginInterface()
        self.interface = interface.get_blacklist_interface()

    def test_interface(self):
        template = '{}_blacklisted_{}'
        methods = ['directories', 'filepaths', 'plugins']
        get_func = lambda attr: getattr(self.interface, attr)

        adders = [get_func(template.format('add',
                                           method)) for method in methods]

        setters = [get_func(template.format('set',
                                            method)) for method in methods]

        getters = [get_func(template.format('get',
                                            method)) for method in methods]

        removers = [get_func(template.format('remove',
                                             method)) for method in methods]
        instance = TestObj()
        second_instance = TestObj()
        for adder, setter, getter, remover in zip(adders, setters,
                                                  getters, removers):

            adder(instance)
            self.assertIn(instance, getter())
            setter(second_instance)
            self.assertIn(second_instance, getter())
            self.assertNotIn(instance, getter())
            remover(second_instance)
            self.assertNotIn(second_instance, getter())
    """
    def test_add_plugin_directories(self):
        added_dir = 'pluginmanager'
        self.interface.add_plugin_directories(added_dir)
        directories = self.interface.get_plugin_directories()
        self.assertIn(added_dir, directories)

    def test_set_plugin_directories(self):
        preset_dir = self.interface.get_plugin_directories().pop()
        set_dir = 'pluginmanager'
        self.interface.set_plugin_directories(set_dir)
        directories = self.interface.get_plugin_directories()
        self.assertIn(set_dir, directories)
        self.assertNotIn(preset_dir, directories)
    """

    def test_set_blacklist_filepath(self):
        filepath = 'test/dir'
        self.interface.set_blacklisted_filepaths(filepath)
        blacklisted = self.interface.get_blacklisted_filepaths()
        self.assertIn(filepath, blacklisted)
