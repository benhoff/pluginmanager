import unittest
from simpleyapsy.interface import Interface


class TestInterface(unittest.TestCase):
    def setUp(self):
        self.test_obj = type('', (), {})
        self.interface = Interface()

    def test_add_plugin_directories(self):
        added_dir = 'simpleyapsy'
        self.interface.add_plugin_directories(added_dir)
        directories = self.interface.get_plugin_directories()
        self.assertIn(added_dir, directories)

    def test_set_plugin_directories(self):
        preset_dir = self.interface.get_plugin_directories().pop()
        set_dir = 'simpleyapsy'
        self.interface.set_plugin_directories(set_dir)
        directories = self.interface.get_plugin_directories()
        self.assertIn(set_dir, directories)
        self.assertNotIn(preset_dir, directories)

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

    def test_get_file_getters(self):
        self.interface.add_file_getters(self.test_obj)
        file_getters = self.interface.get_file_getters()
        self.assertIn(self.test_obj, file_getters)

    def test_locate_plugin_filepaths(self):
        pass

    def test_get_plugin_filepaths(self):
        pass
