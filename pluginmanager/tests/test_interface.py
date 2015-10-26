import unittest
from pluginmanager.interface import Interface
from pluginmanager.iplugin import IPlugin


class TestInterface(unittest.TestCase):
    def setUp(self):
        self.test_obj = IPlugin()
        self.interface = Interface()

    def test_track_site_package_path(self):
        # TODO: better test method
        num_directories = len(self.interface.get_plugin_directories())
        self.interface.track_site_package_paths()
        new_num_dirs = len(self.interface.get_plugin_directories())
        self.assertTrue(new_num_dirs > num_directories)

    def test_adders_getters_and_setters(self):
        adders = ['add_plugin_filepaths',
                  'add_plugins']

        getters = ['get_plugin_filepaths',
                   'get_plugins']

        setters = ['set_plugin_filepaths',
                   'set_plugins']

        all_ = [adders, getters, setters]
        for index, value in enumerate(all_):
            all_[index] = [getattr(self.interface, name) for name in value]
        adders, getters, setters = all_
        test_obj = IPlugin()
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
