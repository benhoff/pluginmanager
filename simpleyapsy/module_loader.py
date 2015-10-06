import os
import sys

import importlib

from simpleyapsy.module_parsers import SubclassParser
from simpleyapsy import util as yapsy_util


class ModuleLoader(object):
    def __init__(self,
                 module_parsers=[SubclassParser()],
                 blacklisted_filepaths=set()):

        self.loaded_modules = set()
        self.processed_filepaths = set()
        self.module_parsers = module_parsers
        self.blacklisted_filepaths = blacklisted_filepaths

    def set_module_parsers(self, module_parsers):
        module_parsers = yapsy_util.return_list(module_parsers)
        self.module_parsers = module_parsers

    def add_module_parsers(self, module_parsers):
        module_parsers = yapsy_util.return_list(module_parsers)
        self.module_parsers.extend(module_parsers)

    def blacklist_filepaths(self, filepaths):
        filepaths = yapsy_util.return_list(filepaths)
        self.blacklisted_filepaths.update(filepaths)

    def set_blacklisted_filepaths(self, filepaths):
        filepaths = yapsy_util.return_list(filepaths)
        filepaths = set(filepaths)
        self.blacklisted_filepaths = filepaths

    def get_blacklisted_filepaths(self):
        return self.blacklisted_filepaths

    def reload_module(self, name):
        module = sys.modules[name]
        importlib.reload(module)

    def get_loaded_modules(self):
        loaded_modules = []
        for name in self.loaded_modules.keys():
            loaded_modules.append(sys.modules[name])
        return loaded_modules

    def get_plugins_from_modules(self):
        plugins = []
        loaded_modules = self.get_loaded_modules()
        for module in loaded_modules:
            for plugin_parser in self.module_parsers:
                plugins.extend(plugin_parser.get_plugins(module))
        return plugins

    def load_modules(self, filepaths):
        # removes filepaths from processed if they are not in sys.modules
        self._update_internal_state()
        # handle case of single filepath passed in
        if not isinstance(filepaths, list) or not isinstance(filepaths, set):
            filepaths = set(filepaths)

        for filepath in filepaths:
            filepath = self._process_filepath(filepath)
            # check to see if blacklisted or already processed
            if not self._valid_filepath(filepath):
                continue

            name = yapsy_util.get_module_name(filepath)
            plugin_module_name = yapsy_util.create_unique_module_name(name)

            spec = importlib.util.spec_from_file_location(plugin_module_name,
                                                          filepath)
            try:
                module = spec.loader.load_module()
                self.loaded_modules.update(module.__name__)
            except ImportError:
                pass

            self.processed_filepaths.add(filepath)

        return self.loaded_modules

    def _process_filepath(self, filepath):
        if (os.path.isdir(filepath) and
                os.path.isfile(os.path.join(filepath, '__init__.py'))):

            filepath = os.path.join(filepath, '__init__.py')

        if not filepath.endswith('.py'):
            filepath += '.py'
        return filepath

    def _valid_filepath(self, filepath):
        valid = True
        if (filepath in self.blacklisted_filepaths or
                filepath in self.processed_filepaths):
            valid = False

        return valid

    def _update_internal_state(self):
        system_modules = sys.modules.keys()
        for module, filepath in self.loaded_modules.items():
            if module not in system_modules:
                self.processed_filepaths.pop(filepath)
                self.loaded_modules.pop(module)
