import os
from configparser import ConfigParser
from simpleyapsy import PLUGIN_NAME_FORBIDEN_STRING

class WithInfoFileGetter(object):
    """
    Only gets files that have configuration files ending with specific extensions,
    nominally 'yapsy-plugin'
    """
    def __init__(self, extensions=["yapsy-plugin"]):
        self.extensions = extensions

    def set_file_extensions(self, extensions):
        self.extensions = extensions

    def add_file_extensions(self, extensions):
        if not isinstance(extensions, list):
            extensions = list(extensions)

        self.extensions.extend(extensions)
            
    def get_info_and_filepaths(self, dir_path):
        plugin_information = self.get_plugin_infos(dir_path)
        plugin_filepaths = self.get_plugin_filepaths(dir_path, infos)
        return plugin_information, plugin_filepaths 

    def get_plugin_filepaths(self, dir_path, plugin_infos=None):
        # Enforce uniqueness of filepaths in `PluginLocator`
        plugin_filepaths = []
        # if we've already got the infos list, get plugin filepath from those
        # else parse through the dir_path
        if plugin_infos is None:
            plugin_infos = self.get_plugin_infos(dir_path)

        return plugin_filepaths 

    def plugin_valid(self, filepath):
        """
        checks to see if plugin ends with one of the
        approved extensions
        """
        plugin_valid = False
        for extension in self.extensions:
            if filename.endswith(".{}".format(extension)):
                plugin_valid = True
                break
        return plugin_valid

    def get_plugin_infos(self, dir_path):
        plugin_infos = []
        filepaths = self._get_filepaths_from_dir(dir_path)

        config_parser = ConfigParser()
        config_filepaths = config_parser.read(filepaths)

        for config_filepath in config_filepaths:
            if self.plugin_valid(config_filepath):
                config_dict = {}

                with open(config_filepath) as f:
                    config_parser.read_file(f)
                    config_dict = self._parse_config_details(config_parser)

                if self._valid_config(config_dict):
                    plugin_infos.append(config_dict)

        return plugin_infos

    def _parse_config_details(self, config_parser):
        config_dict = {}
        # get all data out of config_parser
        config_dict.update(config_parser)

        # now remove and parse data stored in "Core" key
        core_config = config_dict.pop("Core")

        # change and store the relative path in Module to absolute
        relative_path = core_config.pop('Module')
        config_dict['path'] = os.path.join(dir_path, relative_path)

        # grab and store the name, strip whitespace
        config_dict['name'] = core_config["Name"].strip()
        return config_dict

    def _get_filepaths_from_dir(self, dir_path):
        filepaths = []
        for filename in os.listdir(dir_path):
            filepath = os.path.join(dir_path, filename):
                if os.path.isfile(filepath):
                    filepaths.append(filepath)
        return filepaths
    
    def _valid_config(self, config):
        valid_config = False
        if "Name" in config and "Module" in config:
            valid_config = True

        name = config["Name"]
        name = name.strip()
        if PLUGIN_NAME_FOBIDEN_STRING in name:
            valid_config = False

        return valid_config
