import os
import sys

import importlib

from pluginmanager.module_parsers import SubclassParser
from pluginmanager import util as yapsy_util


class ModuleLoader(object):
    def __init__(self,
                 module_parsers=[SubclassParser()],
                 blacklisted_filepaths=set()):

        module_parsers = yapsy_util.return_list(module_parsers)
        self.loaded_modules = set()
        self.processed_filepaths = {}
        self.module_parsers = module_parsers
        self.blacklisted_filepaths = blacklisted_filepaths

    def set_module_parsers(self, module_parsers):
        module_parsers = yapsy_util.return_list(module_parsers)
        self.module_parsers = module_parsers

    def add_module_parsers(self, module_parsers):
        module_parsers = yapsy_util.return_list(module_parsers)
        self.module_parsers.extend(module_parsers)

    def add_blacklisted_filepaths(self, filepaths):
        filepaths = set(yapsy_util.return_list(filepaths))
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

    def _get_modules(self, names):
        loaded_modules = []
        for name in names:
            loaded_modules.append(sys.modules[name])
        return loaded_modules

    def get_loaded_modules(self, names=None):
        return self._get_modules(self.loaded_modules)

    def get_plugins_from_modules(self, modules=None):
        plugins = []
        if modules is None:
            modules = self.get_loaded_modules()
        else:
            modules = yapsy_util.return_list(modules)
        for module in modules:
            for plugin_parser in self.module_parsers:
                plugins.extend(plugin_parser.get_plugins(module))
        return plugins

    def load_modules(self, filepaths):
        # removes filepaths from processed if they are not in sys.modules
        self._update_internal_state()
        # handle case of single filepath passed in
        if not isinstance(filepaths, list) or not isinstance(filepaths, set):
            filepaths = set(filepaths)

        modules = []
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
                self.loaded_modules.add(module.__name__)
                modules.append(module)
            except ImportError:
                pass

            self.processed_filepaths[module.__name__] = filepath

        return modules

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
                filepath in self.processed_filepaths.values()):
            valid = False

        return valid

    def _update_internal_state(self):
        system_modules = sys.modules.keys()
        for module in self.loaded_modules:
            if module not in system_modules:
                self.processed_filepaths.pop(module)
                self.loaded_modules.pop(module)
