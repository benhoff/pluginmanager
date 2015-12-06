import os
import unittest
from pluginmanager import util
from pluginmanager.file_filters import WithInfoFileFilter
from pluginmanager.tests.compat import tempfile
from pluginmanager.compat import FILE_ERROR, ConfigParser


class TestWithInfoFileGetter(unittest.TestCase):
    def setUp(self):
        self.file_filter = WithInfoFileFilter()
        self._plugin_file_name = 'plugin.{}'
        self.tempdir = tempfile.TemporaryDirectory()
        file_template = os.path.join(self.tempdir.name,
                                     self._plugin_file_name)

        open(file_template.format('py'), 'a').close()
        p = self._plugin_file_name[:-3]
        yapsy_contents = """[Core]\nName = Test\nModule = {}\n""".format(p)

        plugin_file = open(file_template.format('yapsy-plugin'), 'w+')
        plugin_file.write(yapsy_contents)
        plugin_file.close()
        self.plugin_filepaths = util.get_filepaths_from_dir(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_callable(self):
        filepaths = self.file_filter(self.plugin_filepaths)
        valid = False
        for filepath in filepaths:
            if os.path.basename(filepath) == 'plugin.py':
                valid = True
                break
        self.assertTrue(valid)

    def test_set_file_extension(self):
        test_extension = 'test'
        self.file_filter.set_file_extensions(test_extension)
        self.assertIn(test_extension, self.file_filter.extensions)

    def test_add_file_extensions(self):
        new_extension = 'test'
        previous_extension = self.file_filter.extensions[0]
        self.file_filter.add_file_extensions(new_extension)
        self.assertIn(new_extension, self.file_filter.extensions)
        self.assertIn(previous_extension, self.file_filter.extensions)

    def test_plugin_valid(self):
        valid_filepath = 'file.yapsy-plugin'
        unvalid_filepath = 'file.bad'
        valid_filepath = self.file_filter.plugin_valid(valid_filepath)
        unvalid_filepath = self.file_filter.plugin_valid(unvalid_filepath)
        self.assertTrue(valid_filepath)
        self.assertFalse(unvalid_filepath)

    def test_get_plugin_info(self):
        plugin_infos = self.file_filter.get_plugin_infos(self.plugin_filepaths)
        plugin_infos = plugin_infos.pop()
        self.assertIn('name', plugin_infos)
        self.assertEqual(plugin_infos['name'], 'Test')

    def test_get_plugin_filepath(self):
        f = self.file_filter.get_plugin_filepaths
        plugin_filepaths = f(self.plugin_filepaths)
        file_name = self._plugin_file_name.format('py')
        python_file = os.path.basename(plugin_filepaths.pop())
        self.assertEqual(file_name, python_file)

    def test_parse_config_details(self):
        base, dir_name = os.path.split(self.tempdir.name)
        config = ConfigParser()
        config.read_dict({"Core": {"Module": base, "Name": 'blah'}})
        dir_path = os.path.join(base, '__init__.py')
        if os.path.isfile(dir_path):
            os.remove(dir_path)

        self.assertRaises(FILE_ERROR,
                          self.file_filter._parse_config_details,
                          config,
                          base)
        open(dir_path, 'a').close()
        config.read_dict({"Core": {"Module": base, "Name": 'test'}})
        config = self.file_filter._parse_config_details(config, base)
        self.assertTrue(config['path'] == dir_path)

    def test_empty_dirs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            info, filepaths = self.file_filter.get_info_and_filepaths(temp_dir)
        self.assertEqual(info, [])
        self.assertEqual(filepaths, set())
