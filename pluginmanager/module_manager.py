import os
import sys
import logging
logging.basicConfig()
import inspect
from .compat import load_source

from pluginmanager import util as manager_util


class ModuleManager(object):
    def __init__(self, module_filters=None):
        if module_filters is None:
            module_filters = []
        module_filters = manager_util.return_list(module_filters)

        self.loaded_modules = set()
        self.processed_filepaths = {}
        self.module_filters = module_filters
        self._log = logging.getLogger(__name__)
        self._error_string = 'pluginmanager unable to import {}\n'

    def set_module_filters(self, module_filters):
        """
        Sets the internal module filters to `module_filters`
        `module_filters` may be a single object or an iterable.

        Every module filters must be a callable and take in
        a list of plugins and their associated names.
        """
        module_filters = manager_util.return_list(module_filters)
        self.module_filters = module_filters

    def add_module_filters(self, module_filters):
        """
        Adds `module_filters` to the internal module filters.
        May be a single object or an iterable.

        Every module filters must be a callable and take in
        a list of plugins and their associated names.
        """
        module_filters = manager_util.return_list(module_filters)
        self.module_filters.extend(module_filters)

    def get_module_filters(self, filter_function=None):
        """
        Gets the internal module filters. Returns a list object.

        If supplied, the `filter_function` should take in a single
        list argument and return back a list. `filter_function` is
        designed to given the option for a custom filter on the module filters.
        """
        if filter_function is None:
            return self.module_filters
        else:
            return filter_function(self.module_filters)

    def remove_module_filters(self, module_filters):
        """
        Removes `module_filters` from the internal module filters.
        If the filters are not found in the internal representation,
        the function passes on silently.

        `module_filters` may be a single object or an iterable.
        """
        manager_util.remove_from_list(self.module_filters, module_filters)

    def _get_modules(self, names):
        """
        An internal method that gets the `names` from sys.modules and returns
        them as a list
        """
        loaded_modules = []
        for name in names:
            loaded_modules.append(sys.modules[name])
        return loaded_modules

    def add_to_loaded_modules(self, modules):
        """
        Manually add in `modules` to be tracked by the module manager.

        `moduels` may be a single object or an iterable.
        """
        modules = manager_util.return_set(modules)
        for module in modules:
            if not isinstance(module, str):
                module = module.__name__
            self.loaded_modules.add(module)

    def get_loaded_modules(self):
        """
        Returns all modules loaded by this instance.
        """
        return self._get_modules(self.loaded_modules)

    def collect_plugins(self, modules=None):
        """
        Collects all the plugins from `modules`.
        If modules is None, collects the plugins from the loaded modules.

        All plugins are passed through the module filters, if any are any,
        and returned as a list.
        """
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
        """
        Internal helper method to parse all of the plugins and names
        through each of the module filters
        """
        if self.module_filters:
            module_plugins = set()
            for module_filter in self.module_filters:
                module_plugins.update(module_filter(plugins, names))
            plugins = module_plugins
        return plugins

    def load_modules(self, filepaths):
        """
        Loads the modules from their `filepaths`. A filepath may be
        a directory filepath if there is an `__init__.py` file in the
        directory.

        If a filepath errors, the exception will be caught and logged
        in the logger.

        Returns a list of modules.
        """
        # removes filepaths from processed if they are not in sys.modules
        self._update_loaded_modules()
        filepaths = manager_util.return_set(filepaths)

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

        return modules

    def _process_filepath(self, filepath):
        """
        processes the filepath by checking if it is a directory or not
        and adding `.py` if not present.
        """
        if (os.path.isdir(filepath) and
                os.path.isfile(os.path.join(filepath, '__init__.py'))):

            filepath = os.path.join(filepath, '__init__.py')

        if not filepath.endswith('.py'):
            filepath += '.py'
        return filepath

    def _valid_filepath(self, filepath):
        """
        checks to see if the filepath has already been processed
        """
        valid = True
        if filepath in self.processed_filepaths.values():
            valid = False

        return valid

    def _update_loaded_modules(self):
        """
        Updates the loaded modules by checking if they are still in sys.modules
        """
        system_modules = sys.modules.keys()
        for module in list(self.loaded_modules):
            if module not in system_modules:
                self.processed_filepaths.pop(module)
                self.loaded_modules.remove(module)
