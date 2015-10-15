import builtins
import os
from configparser import ConfigParser
from simpleyapsy import util
from . import PLUGIN_FORBIDDEN_NAME

# Work around for python 3.2
FILE_ERROR = getattr(builtins,
                     "FileNotFoundError",
                     getattr(builtins, "OSError"))


class WithInfoFileGetter(object):
    """
    Only gets files that have configuration files ending with specific
    extensions, nominally 'yapsy-plugin'
    """
    def __init__(self, extensions=["yapsy-plugin"]):
        self.extensions = extensions

    def set_file_extensions(self, extensions):
        extensions = util.return_list(extensions)
        self.extensions = extensions

    def add_file_extensions(self, extensions):
        extensions = util.return_list(extensions)
        self.extensions.extend(extensions)

    def get_info_and_filepaths(self, dir_path):
        plugin_information = self.get_plugin_infos(dir_path)
        plugin_filepaths = self.get_plugin_filepaths(dir_path,
                                                     plugin_information)

        return plugin_information, plugin_filepaths

    def get_plugin_filepaths(self, dir_path, plugin_infos=None):
        # Enforce uniqueness of filepaths in `PluginLocator`
        plugin_filepaths = set()
        # if we've already got the infos list, get plugin filepath from those
        # else parse through the dir_path
        if plugin_infos is None:
            plugin_infos = self.get_plugin_infos(dir_path)

        for plugin_info in plugin_infos:
            path = plugin_info['path']
            plugin_filepaths.add(path)

        return plugin_filepaths

    def plugin_valid(self, filepath):
        """
        checks to see if plugin ends with one of the
        approved extensions
        """
        plugin_valid = False
        for extension in self.extensions:
            if filepath.endswith(".{}".format(extension)):
                plugin_valid = True
                break
        return plugin_valid

    def get_plugin_infos(self, dir_path):
        plugin_infos = []
        filepaths = util.get_filepaths_from_dir(dir_path)

        config_parser = ConfigParser()
        config_filepaths = config_parser.read(filepaths)

        for config_filepath in config_filepaths:
            if self.plugin_valid(config_filepath):
                config_dict = {}

                with open(config_filepath) as f:
                    config_parser.read_file(f)
                    config_dict = self._parse_config_details(config_parser,
                                                             dir_path)

                if self._valid_config(config_dict):
                    plugin_infos.append(config_dict)

        return plugin_infos

    def _parse_config_details(self, config_parser, dir_path):
        config_dict = {}
        # get all data out of config_parser
        config_dict.update(config_parser)

        # now remove and parse data stored in "Core" key
        core_config = config_dict.pop("Core")

        # change and store the relative path in Module to absolute
        relative_path = core_config.pop('Module')
        path = os.path.join(dir_path, relative_path)

        if os.path.isfile(path + '.py'):
            path += '.py'
        elif (os.path.isdir(path) and
                os.path.isfile(os.path.join(path, '__init__.py'))):
            path = os.path.join(path, '__init__.py')
        else:
            raise FILE_ERROR('{} not a `.py` file or a dir'.format(path))

        config_dict['path'] = path

        # grab and store the name, strip whitespace
        config_dict['name'] = core_config["Name"].strip()
        return config_dict

    def _valid_config(self, config):
        valid_config = False
        if "name" in config and "path" in config:
            valid_config = True

        name = config['name']
        name = name.strip()
        if PLUGIN_FORBIDDEN_NAME in name:
            valid_config = False

        return valid_config
