import os
import unittest
import tempfile
from simpleyapsy.file_getters import WithInfoFileGetter


class TestWithInfoFileGetter(unittest.TestCase):
    def setUp(self):
        self.file_getter = WithInfoFileGetter()

    def test_set_file_extension(self):
        test_extension = 'test'
        self.file_getter.set_file_extensions(test_extension)
        self.assertIn(test_extension, self.file_getter.extensions)

    def test_add_file_extensions(self):
        new_extension = 'test'
        previous_extension = self.file_getter.extensions[0]
        self.file_getter.add_file_extensions(new_extension)
        self.assertIn(new_extension, self.file_getter.extensions)
        self.assertIn(previous_extension, self.file_getter.extensions)

    def test_plugin_valid(self):
        valid_filepath = 'file.yapsy-plugin'
        unvalid_filepath = 'file.bad'
        valid_filepath = self.file_getter.plugin_valid(valid_filepath)
        unvalid_filepath = self.file_getter.plugin_valid(unvalid_filepath)
        self.assertTrue(valid_filepath)
        self.assertFalse(unvalid_filepath)

    def test_get_plugin_info(self):
        with tempfile.TemporaryDirectory() as test_dir:
            file_template = os.path.join(test_dir, 'plugin.{}')
            plugin_file = open(file_template.format('yapsy-plugin'), 'w+')
            fake_python = open(file_template.format('py'), 'w+')

            python_file_name = fake_python.name[:-3]
            yapsy_contents = """
            [Core]\n
            Name = Test\n
            Module = {}\n""".format(python_file_name)

            plugin_file.write(yapsy_contents)
            plugin_file.close()
            fake_python.close()
            info = self.file_getter.get_plugin_infos(test_dir)
        self.assertNotEqual(info, [])

    def test_get_plugin_filepath(self):
        with tempfile.TemporaryDirectory() as test_dir:
            file_template = os.path.join(test_dir, 'plugin.{}')
            plugin_file = open(file_template.format('yapsy-plugin'), 'w+')
            fake_python = open(file_template.format('py'), 'w+')

            python_file_name = fake_python.name[:-3]
            yapsy_contents = """
            [Core]\n
            Name = Test\n
            Module = {}\n""".format(python_file_name)

            plugin_file.write(yapsy_contents)
            plugin_file.close()
            fake_python.close()
            files = self.file_getter.get_plugin_filepaths(test_dir)
        self.assertIn(fake_python.name, files)
