import os
import unittest
from pluginmanager.tests.compat import tempfile
from pluginmanager.compat import FILE_ERROR, ConfigParser

from pluginmanager.file_filters import WithInfoFileFilter


class TestWithInfoFileGetter(unittest.TestCase):
    def setUp(self):
        self.file_filter = WithInfoFileFilter()
        self._plugin_file_name = 'plugin.{}'

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

    def _create_tempfiles(self):
        with tempfile.TemporaryDirectory() as test_dir:
            file_template = os.path.join(test_dir,
                                         self._plugin_file_name)

            plugin_file = open(file_template.format('yapsy-plugin'), 'w+')
            open(file_template.format('py'), 'a').close()
            name = self._plugin_file_name[:-3]
            contents = """[Core]\nName = Test\nModule = {}\n""".format(name)

            plugin_file.write(contents)
            plugin_file.close()
            info = self.file_filter.get_plugin_infos(test_dir)
            files = self.file_filter.get_plugin_filepaths(test_dir)
        return info, files

    def test_get_plugin_info(self):
        info, _ = self._create_tempfiles()
        self.assertNotEqual(info, [])

    def test_get_plugin_filepath(self):
        _, files = self._create_tempfiles()
        file_name = self._plugin_file_name.format('py')
        python_file = os.path.basename(files.pop())
        self.assertEqual(file_name, python_file)

    def test_parse_config_details(self):
        dir_path = os.path.dirname(__file__)
        base, dir_name = os.path.split(dir_path)
        parser = ConfigParser()
        parser.read_dict({"Core": {"Module": dir_name}})
        self.assertRaises(FILE_ERROR,
                          self.file_filter._parse_config_details,
                          parser,
                          'invalid/dir')

        parser.read_dict({"Core": {"Module": dir_name, "Name": 'test'}})
        config = self.file_filter._parse_config_details(parser, base)
        dir_path = os.path.join(dir_path, '__init__.py')
        self.assertTrue(config['path'] == dir_path)

    def test_empty_dirs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            info, filepaths = self.file_filter.get_info_and_filepaths(temp_dir)
        self.assertEqual(info, [])
        self.assertEqual(filepaths, set())
