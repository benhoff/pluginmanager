import unittest
from pluginmanager.interface import Interface


class TestInterface(unittest.TestCase):
    def setUp(self):
        self.test_obj = type('', (), {})
        self.interface = Interface()
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

    def test_track_site_package_path(self):
        # TODO: better test method
        num_directories = len(self.interface.get_plugin_directories())
        self.interface.track_site_package_paths()
        new_num_dirs = len(self.interface.get_plugin_directories())
        self.assertTrue(new_num_dirs > num_directories)

    def test_set_file_getters(self):
        self.interface.set_file_getters(self.test_obj)
        file_getters = self.interface.get_file_getters()
        self.assertIn(self.test_obj, file_getters)

    def test_add_get_modules(self):
        pass

    def test_adders_getters_and_setters(self):
        add = ['add_blacklisted_filepaths',
                'add_file_getters',
                'add_instances',
                'add_plugin_directories',
                'add_plugin_filepaths',
                'add_plugins']

        add = [getattr(self.interface, name) for name in add]

        get = ['get_blacklisted_filepaths',
                'get_file_getters',
                'get_instances',
                'get_plugin_directories',
                'get_plugin_filepaths',
                'get_plugins']

        get = [getattr(self.interface, name) for name in get]

        set = ['set_blacklisted_filepaths',
                'set_file_getters',
                'set_instances',
                'set_plugin_directories',
                'set_plugin_filepaths',
                'set_plugins']

        set = [getattr(self.interface, name) for name in set]
        for adder in add:
            adder(self.test_obj)

        for index, value in got:
            self.assertIn(self.test_obj, value())

        file_getters = self.interface.get_file_getters()
        self.assertIn(self.test_obj, file_getters)

    def test_set_plugins(self):
        self.interface.set_plugins(self.test_obj)
        plugins = self.interface.get_plugins()
        self.assertIn(self.test_obj, plugins)

    def test_set_instances(self):
        test_obj = self.test_obj()
        self.interface.set_instances(test_obj)
        instances = self.interface.get_instances()
        self.assertIn(test_obj, instances)

    def test_set_blacklist_filepath(self):
        filepath = 'test/dir'
        self.interface.set_blacklisted_filepaths(filepath)
        blacklisted = self.interface.get_blacklisted_filepaths()
        self.assertIn(filepath, blacklisted)

    def test_locate_plugin_filepaths(self):
        pass

    def test_get_plugin_filepaths(self):
        pass
