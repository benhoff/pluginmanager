import os
import sys
import logging
logging.basicConfig()
import inspect
from .compat import load_source

from pluginmanager import util as manager_util


class ModuleManager(object):
    def __init__(self,
                 module_filters=None,
                 blacklisted_filepaths=None):
        if module_filters is None:
            module_filters = []
        if blacklisted_filepaths is None:
            blacklisted_filepaths = set()
        module_filters = manager_util.return_list(module_filters)

        self.loaded_modules = set()
        self.processed_filepaths = {}
        self.module_filters = module_filters
        self.blacklisted_filepaths = blacklisted_filepaths
        self._log = logging.getLogger(__name__)
        self._error_string = 'pluginmanager unable to import {}\n'

    def set_module_filters(self, module_filters):
        module_filters = manager_util.return_list(module_filters)
        self.module_filters = module_filters

    def add_module_filters(self, module_filters):
        module_filters = manager_util.return_list(module_filters)
        self.module_filters.extend(module_filters)

    def get_module_filters(self, filter_function=None):
        if filter_function is None:
            return self.module_filters
        else:
            return filter_function(self.module_filters)

    def remove_module_filters(self, module_filters):
        manager_util.remove_from_list(self.module_filters, module_filters)

    def add_blacklisted_filepaths(self, filepaths):
        filepaths = set(manager_util.return_list(filepaths))
        self.blacklisted_filepaths.update(filepaths)

    def set_blacklisted_filepaths(self, filepaths):
        filepaths = manager_util.return_list(filepaths)
        filepaths = set(filepaths)
        self.blacklisted_filepaths = filepaths

    def get_blacklisted_filepaths(self):
        return self.blacklisted_filepaths

    def _get_modules(self, names):
        loaded_modules = []
        for name in names:
            loaded_modules.append(sys.modules[name])
        return loaded_modules

    def add_to_loaded_modules(self, modules):
        modules = set(manager_util.return_list(modules))
        for module in modules:
            if not isinstance(module, str):
                module = module.__name__
            self.loaded_modules.add(module)

    def get_loaded_modules(self):
        return self._get_modules(self.loaded_modules)

    def collect_plugins(self, modules=None):
        plugins = []
        if modules is None:
            modules = self.get_loaded_modules()
        else:
            modules = manager_util.return_list(modules)
        for module in modules:
            module_plugins = [(item[1], item[0])
                              for item
                              in inspect.getmembers(module)
                              if item[1] and item[0] != '__builtins__']
            module_plugins, names = zip(*module_plugins)

            module_plugins = self._filter_modules(module_plugins, names)
            plugins.extend(module_plugins)
        return plugins

    def _filter_modules(self, plugins, names):
        if self.module_filters:
            module_plugins = []
            for module_filter in self.module_filters:
                module_plugins.extend(module_filter(plugins, names))
            plugins = module_plugins
        return plugins

    def load_modules(self, filepaths):
        # removes filepaths from processed if they are not in sys.modules
        self._update_internal_state()
        filepaths = manager_util.return_list(filepaths)

        modules = []
        for filepath in filepaths:
            filepath = self._process_filepath(filepath)
            # check to see if blacklisted or already processed
            if not self._valid_filepath(filepath):
                continue

            name = manager_util.get_module_name(filepath)
            plugin_module_name = manager_util.create_unique_module_name(name)

            try:
                module = load_source(plugin_module_name, filepath)
                self.loaded_modules.add(module.__name__)
                modules.append(module)
                self.processed_filepaths[module.__name__] = filepath
            except Exception:
                exc_info = sys.exc_info()
                self._log.error(msg=self._error_string.format(filepath),
                                exc_info=exc_info)

                # self.processed_filepaths['error'] = filepath

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
        for module in list(self.loaded_modules):
            if module not in system_modules:
                self.processed_filepaths.pop(module)
                self.loaded_modules.remove(module)
