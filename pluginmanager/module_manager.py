import os
import sys
import inspect
import importlib

from pluginmanager import util as manager_util


class ModuleManager(object):
    def __init__(self,
                 module_filters=[],
                 blacklisted_filepaths=set()):

        module_filters = manager_util.return_list(module_filters)
        self.loaded_modules = set()
        self.processed_filepaths = {}
        self.module_filters = module_filters
        self.blacklisted_filepaths = blacklisted_filepaths

    def set_module_filters(self, module_filters):
        module_filters = manager_util.return_list(module_filters)
        self.module_filters = module_filters

    def add_module_filters(self, module_filters):
        module_filters = manager_util.return_list(module_filters)
        self.module_filters.extend(module_filters)

    def get_module_filters(self):
        return self.module_filters

    def remove_module_filters(self, module_filters):
        module_filters = manager_util.return_list(module_filters)
        for module_filter in module_filters:
            self.module_filters.remove(module_filter)

    def add_blacklisted_filepaths(self, filepaths):
        filepaths = set(manager_util.return_list(filepaths))
        self.blacklisted_filepaths.update(filepaths)

    def set_blacklisted_filepaths(self, filepaths):
        filepaths = manager_util.return_list(filepaths)
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

    def collect_plugins(self, modules=None):
        plugins = []
        if modules is None:
            modules = self.get_loaded_modules()
        else:
            modules = manager_util.return_list(modules)
        for module in modules:
            module_plugins = [item[1]
                              for item
                              in inspect.getmembers(module)
                              if not isinstance(item[1], dict)]

            module_plugins = self._filter_modules(module_plugins)
            plugins.extend(module_plugins)
        return plugins

    def _filter_modules(self, plugins):
        if self.module_filters:
            module_plugins = []
            for module_filter in self.module_filters:
                module_plugins.extend(module_filter(plugins))
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
        for module in list(self.loaded_modules):
            if module not in system_modules:
                self.processed_filepaths.pop(module)
                self.loaded_modules.remove(module)
