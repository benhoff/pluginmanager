import os
import sys
import inspect
from importlib.machinery import SourceFileLoader
from simpleyapsy import plugin_validators

def _get_unique_module_name(plugin_info):
    plugin_module_name = 'yapsy_plugin_{name}'.format(plugin_info['name'])
    plugin_module_name += '_{number}'
    number = 0
    while True:
        plugin_module_name.format(number)
        if not plugin_module_name in sys.modules:
            break
        number += 1

    return plugin_module_name

class PluginLoader(object):
    def __init__(self,
                 module_parser=[plugin_validators.IsSubclass()]):
        self.loaded_plugins = []
        self.processed_filepaths = []
        self.blacklisted_filepaths = []
        self.module_parser = module_parser

    def add_module_parser(self, plugin_validator):
        if not isinstance(plugin_validator, list):
            plugin_validator = list(plugin_validator)
        self.module_parser.extend(plugin_validator)

    def set_module_parser(self, plugin_validator):
        if not isinstance(plugin_validator, list):
            plugin_validator = list(plugin_validator)
        self.module_parser = plugin_validator

    def blacklist_plugin(self, filepath):
        self.blacklisted_filepaths.append(filepath)

    def get_blacklisted_filepaths(self):
        return self.blacklisted_filepaths

    def load_plugin(self, plugin_locations, plugin_infos=None):
        """
        returns a list of loaded plugins
        """
        for plugin_filepath in plugin_filepaths:
            if plugin_filepath in self.blacklisted_filepaths or plugin_filepath in self.processed_filepaths:
                continue

            if '__init__' in os.path.basename(plugin_filepath)
                plugin_filepath = os.path.dirname(plugin_filepath)

            # NOTE: not sure if req'd or not
            plugin_module_name = _get_unique_module_name(plugin_info)

            try:
                module = SourceFileLoader(plugin_module_name, plugin_filepath)
                if module.is_package():
                    # TODO: Implement
                    pass
                
                # NOTE: looks like `load_module` is deprecated `exec_module`
                module = module.exec_module()
                self.processed_filepaths.append(plugin_filepath)

                for attribute in dir(module):
                    attribute = getattr(module, attribute)
                    for parser in self.module_parser:
                        if parser.is_valid(attribute):
                            self.loaded_plugins.append(attribute)

            except Exception:
                pass

    return self.loaded_plugins
