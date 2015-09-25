import os
import sys
from importlib import util
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
        self.loaded_modules = []
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
        self._update_module_state()

    def reload_plugins(self):
        self._update_module_state()

    def load_plugin(self, plugin_locations, plugin_infos=None):
        """
        returns a list of loaded plugins
        """
        self._update_module_state()
        for plugin_filepath in plugin_filepaths:

            if not self._valid_filepath(plugin_filepath):
                continue

            if os.path.isdir(plugin_filepath) and os.path.isfile(os.path.join(plugin_filepath, '__init__.py')):
                plugin_filepath = os.path.join(plugin_filepath, '__init__.py')

            if not plugin_filepath.endswith('.py'):
                plugin_filepath += '.py'

            # NOTE: not sure if req'd or not
            plugin_module_name = _get_unique_module_name(plugin_info)
            try:
                file_spec = util.spec_from_file_location(plugin_module_name, plugin_filepath)
                loader = file_spec.loader
                module = loader.load_module()
                self.loaded_modules.append(module.__name__)

            except Exception:
                pass

        return self.loaded_plugins

    def _update_module_state(self):
        system_modules = sys.modules.values()
        for loaded_module in self.loaded_modules:
            if not loaded_module in system_modules:
                path = loaded_module.__path__
                if path in self.processed_filepaths:
                    self.processed_filepaths.remove(path)
                self.loaded_modules.remove(loaded_module)
