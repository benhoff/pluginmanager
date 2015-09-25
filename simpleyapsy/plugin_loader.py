import os
import sys
from importlib.machinery import SourceFileLoader
from simpleyapsy import plugin_getters

def _get_unique_module_name(plugin_info):
    module_template= 'yapsy_plugin_{name}'.format(plugin_info['name'])
    module_template += '_{number}'
    number = 0
    while True:
        module_name = module_template.format(number)
        if not module_name in sys.modules:
            break
        number += 1

    return module_name

class PluginLoader(object):
    def __init__(self):

        self.loaded_plugins = []
        self.processed_filepaths = []
        self.blacklisted_filepaths = []

    def blacklist_plugin(self, filepath):
        self.blacklisted_filepaths.append(filepath)

    def get_blacklisted_filepaths(self):
        return self.blacklisted_filepaths

    def _valid_filepath(self, filepath):
        valid = True 
        if filepath in self.blacklisted_filepaths:
            valid = False

        if filepath in self.processed_filepaths:
            valid = False

        return valid

    def load_filepath(self, filepath):
        pass

    def load_plugin(self, plugin_locations, plugin_infos=None):
        """
        returns a list of loaded plugins
        """
        for plugin_filepath in plugin_filepaths:

            if not self._valid_filepath(plugin_filepath):
                continue

            if plugin_filepath.endswith('.py'):
                plugin_filepath = plugin_filepath[:-3]

            if '__init__' in os.path.basename(plugin_filepath)
                plugin_filepath = os.path.dirname(plugin_filepath)

            # NOTE: not sure if req'd or not
            plugin_module_name = _get_unique_module_name(plugin_info)
            try:
                module = SourceFileLoader(plugin_module_name, plugin_filepath)
                module = module.exec_module()
                plugins = self._plugin_validator_iter_helper(module)
                self.loaded_plugins.extend(plugins)

            except Exception:
                pass

        return self.loaded_plugins
