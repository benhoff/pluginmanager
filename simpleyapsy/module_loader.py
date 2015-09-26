import os
import sys
import importlib
from importlib import util
from simpleyapsy import plugin_getters

class ModuleLoader(object):
    def __init__(self):
        self.loaded_modules = {}
        self.processed_filepaths = []
        self.blacklisted_filepaths = []

    def blacklist_filepaths(self, filepaths):
        if not isinstance(filepaths, list):
            filepaths = list(filepaths)
        self.blacklisted_filepaths.extend(filepaths)

    def get_blacklisted_filepaths(self):
        return self.blacklisted_filepaths

    def set_blacklisted_filepaths(self, filepaths):
        if not isinstance(filepaths, list):
            filepaths = list(filepaths)
        self.blacklisted_filepaths = filepaths

    def reload_module(self, name):
        self._update_internal_state()
        module = sys.modules[name]
        importlib.reload(module)

    def get_loaded_modules(self):
        loaded_modules = []
        for name in self.loaded_modules.keys():
            loaded_modules.append(sys.modules[name])
        return loaded_modules

    def load_modules(self, filepaths):
        """
        returns a list of loaded modules
        """
        if not isinstance(pluign_filepaths, list):
            plugin_filepaths = list(plugin_filepaths)

        self._update_internal_state()
        for plugin_filepath in plugin_filepaths:
            if not self._valid_filepath(plugin_filepath):
                continue

            if os.path.isdir(plugin_filepath) and os.path.isfile(os.path.join(plugin_filepath, '__init__.py')):
                plugin_filepath = os.path.join(plugin_filepath, '__init__.py')

            if not plugin_filepath.endswith('.py'):
                plugin_filepath += '.py'
            
            # FIXME
            plugin_module_name = _create_unique_module_name(plugin_info)
            try:
                module = self._load_module(plugin_filepath)
                self.loaded_modules[module.__name__] = module.__path__

            except Exception:
                pass

        return self.loaded_plugins

    def _valid_filepath(self, filepath):
        valid = True 
        if filepath in self.blacklisted_filepaths:
            valid = False

        if filepath in self.processed_filepaths:
            valid = False

        return valid

    def _load_module(self, filepath):
        """
        To be used for compatability
        """
        file_spec = util.spec_from_file_location(plugin_module_name, plugin_filepath)
        loader = file_spec.loader
        module = loader.load_module()
        return module

    def _update_internal_state(self):
        system_modules = sys.modules.keys()
        for module, filepath in self.loaded_modules.items():
            if not module in system_modules:
                self.processed_filepaths.remove(filepath)
                self.loaded_modules.pop(module)

# TODO: move me
def _create_unique_module_name(plugin_info):
    module_template= 'yapsy_plugin_{name}'.format(plugin_info['name'])
    module_template += '_{number}'
    number = 0
    while True:
        module_name = module_template.format(number)
        if not module_name in sys.modules:
            break
        number += 1

    return module_name
