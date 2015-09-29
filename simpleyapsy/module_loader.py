import os
import sys
import types

import importlib
from importlib import util

from simpleyapsy.module_parsers import SubclassParser
from simpleyapsy import util

class ModuleLoader(object):
    def __init__(self, module_parsers=[SubclassParser()]):
        self.module_parsers = module_parsers
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
        # removes filepaths from processed if they are not in sys.modules
        self._update_internal_state()
        if isinstance(filepaths, dict):
            filepaths = filepaths.keys()
            plugin_infos = filepaths.values()
        # handle case of single filepath passed in
        if not isinstance(filepaths, list) and not isinstance(filepaths, types.GeneratorType):
            filepaths = list(filepaths)

        for index, filepath in enumerate(filepaths):
            filepath = self._process_filepath(filepath)
            # check to see if blacklisted or already processed
            if not self._valid_filepath(filepath):
                continue
            try:
                plugin_info = plugin_infos[index]
                plugin_module_name = _create_unique_module_name(plugin_info)
            except NameError:
                # no plugin_info object, so let's make one
                name = util.get_module_name(filepath)
                plugin_info = {'path':filepath, 'name':name}
                plugin_module_name = util.create_unique_module_name(name)

            spec = importlib.util.spec_from_file_location(plugin_module_name, filepath)
            try:
                module = spec.loader.load_module()
                self.loaded_modules[module.__name__] = plugin_info
            except ImportError:
                pass

            self.processed_filepaths.append(filepath)

        return self.loaded_modules

    def _process_filepath(self, filepath):
        if os.path.isdir(filepath) and os.path.isfile(os.path.join(filepath, '__init__.py')):
            filepath = os.path.join(filepath, '__init__.py')

        if not filepath.endswith('.py'):
            filepath += '.py'
        return filepath

    def _valid_filepath(self, filepath):
        valid = True 
        if filepath in self.blacklisted_filepaths or filepath in self.processed_filepaths:
            valid = False

        return valid

    def _update_internal_state(self):
        system_modules = sys.modules.keys()
        for module, filepath in self.loaded_modules.items():
            if not module in system_modules:
                self.processed_filepaths.remove(filepath)
                self.loaded_modules.pop(module)
