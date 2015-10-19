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

    def test_add_get_modules(self):
        pass

    def test_instance_manager(self):
        pass

    def test_plugin_directories(self):
        pass

    def test_adders_getters_and_setters(self):
        adders = ['add_blacklisted_filepaths',
                  'add_file_filters',
                  'add_plugin_filepaths',
                  'add_plugins']

        getters = ['get_blacklisted_filepaths',
                   'get_file_filters',
                   'get_plugin_filepaths',
                   'get_plugins']

        setters = ['set_blacklisted_filepaths',
                   'set_file_filters',
                   'set_plugin_filepaths',
                   'set_plugins']

        all = [adders, getters, setters]
        for index, value in enumerate(all):
            all[index] = [getattr(self.interface, name) for name in value]
        adders, getters, setters = all
        test_obj = type('', (), {})
        for index, (adder, getter, setter) in enumerate(zip(adders,
                                                            getters,
                                                            setters)):
            adder(self.test_obj)
            self.assertIn(self.test_obj,
                          getter(),
                          '{} not found in {} from {}'.format(self.test_obj,
                                                              getter(),
                                                              adder))

            setter(test_obj)
            self.assertIn(test_obj, getter())
            self.assertNotIn(self.test_obj, getter())

    def test_set_plugins(self):
        self.interface.set_plugins(self.test_obj)
        plugins = self.interface.get_plugins()
        self.assertIn(self.test_obj, plugins)

    def test_set_blacklist_filepath(self):
        filepath = 'test/dir'
        self.interface.set_blacklisted_filepaths(filepath)
        blacklisted = self.interface.get_blacklisted_filepaths()
        self.assertIn(filepath, blacklisted)

    def test_locate_plugin_filepaths(self):
        pass

    def test_get_plugin_filepaths(self):
        pass
