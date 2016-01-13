import os
import sys
import logging
import inspect
from .compat import load_source

from pluginmanager import util

logging.basicConfig()


class ModuleManager(object):
    """
    `ModuleManager` manages the module plugin filter state and is responsible
    for both loading the modules from source code and collecting the plugins
    from each of the modules.

    `ModuleManager` can also optionally manage modules explicitly through
    the use of the add/get/set loaded modules methods. The default
    implementation is hardwired to use the tracked loaded modules if no
    modules are passed into the `collect_plugins` method.
    """
    def __init__(self, module_plugin_filters=None):
        """
        `module_plugin_filters` are callable filters. Each filter must take
        in a list of plugins and a list of plugin names in the form of:

        ::

            def my_module_plugin_filter(plugins: list, plugin_names: list):
                pass

        `module_plugin_filters` should return a list of the plugins and may
        be either a single object or an iterable.
        """
        if module_plugin_filters is None:
            module_plugin_filters = []
        module_plugin_filters = util.return_list(module_plugin_filters)
        self.loaded_modules = set()
        self.processed_filepaths = dict()
        self.module_plugin_filters = module_plugin_filters
        self._log = logging.getLogger(__name__)
        self._error_string = 'pluginmanager unable to import {}\n'

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
        filepaths = util.return_set(filepaths)

        modules = []
        for filepath in filepaths:
            filepath = self._clean_filepath(filepath)
            # check to see if already processed and move onto next if so
            if self._processed_filepath(filepath):
                continue

            module_name = util.get_module_name(filepath)
            plugin_module_name = util.create_unique_module_name(module_name)

            try:
                module = load_source(plugin_module_name, filepath)
            # Catch all exceptions b/c loader will return errors
            # within the code itself, such as Syntax, NameErrors, etc.
            except Exception:
                exc_info = sys.exc_info()
                self._log.error(msg=self._error_string.format(filepath),
                                exc_info=exc_info)
                continue

            self.loaded_modules.add(module.__name__)
            modules.append(module)
            self.processed_filepaths[module.__name__] = filepath

        return modules

    def collect_plugins(self, modules=None):
        """
        Collects all the plugins from `modules`.
        If modules is None, collects the plugins from the loaded modules.

        All plugins are passed through the module filters, if any are any,
        and returned as a list.
        """
        if modules is None:
            modules = self.get_loaded_modules()
        else:
            modules = util.return_list(modules)

        plugins = []
        for module in modules:
            module_plugins = [(item[1], item[0])
                              for item
                              in inspect.getmembers(module)
                              if item[1] and item[0] != '__builtins__']
            module_plugins, names = zip(*module_plugins)

            module_plugins = self._filter_modules(module_plugins, names)
            plugins.extend(module_plugins)
        return plugins

    def set_module_plugin_filters(self, module_plugin_filters):
        """
        Sets the internal module filters to `module_plugin_filters`
        `module_plugin_filters` may be a single object or an iterable.

        Every module filters must be a callable and take in
        a list of plugins and their associated names.
        """
        module_plugin_filters = util.return_list(module_plugin_filters)
        self.module_plugin_filters = module_plugin_filters

    def add_module_plugin_filters(self, module_plugin_filters):
        """
        Adds `module_plugin_filters` to the internal module filters.
        May be a single object or an iterable.

        Every module filters must be a callable and take in
        a list of plugins and their associated names.
        """
        module_plugin_filters = util.return_list(module_plugin_filters)
        self.module_plugin_filters.extend(module_plugin_filters)

    def get_module_plugin_filters(self, filter_function=None):
        """
        Gets the internal module filters. Returns a list object.

        If supplied, the `filter_function` should take in a single
        list argument and return back a list. `filter_function` is
        designed to given the option for a custom filter on the module filters.
        """
        if filter_function is None:
            return self.module_plugin_filters
        else:
            return filter_function(self.module_plugin_filters)

    def remove_module_plugin_filters(self, module_plugin_filters):
        """
        Removes `module_plugin_filters` from the internal module filters.
        If the filters are not found in the internal representation,
        the function passes on silently.

        `module_plugin_filters` may be a single object or an iterable.
        """
        util.remove_from_list(self.module_plugin_filters,
                              module_plugin_filters)

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

        `modules` may be a single object or an iterable.
        """
        modules = util.return_set(modules)
        for module in modules:
            if not isinstance(module, str):
                module = module.__name__
            self.loaded_modules.add(module)

    def get_loaded_modules(self):
        """
        Returns all modules loaded by this instance.
        """
        return self._get_modules(self.loaded_modules)

    def _filter_modules(self, plugins, names):
        """
        Internal helper method to parse all of the plugins and names
        through each of the module filters
        """
        if self.module_plugin_filters:
            # check to make sure the number of plugins isn't changing
            original_length_plugins = len(plugins)
            module_plugins = set()
            for module_filter in self.module_plugin_filters:
                module_plugins.update(module_filter(plugins, names))
                if len(plugins) < original_length_plugins:
                    warning = """Module Filter removing plugins from original
                    data member! Suggest creating a new list in each module
                    filter and returning new list instead of modifying the
                    original data member so subsequent module filters can have
                    access to all the possible plugins.\n {}"""

                    self._log.info(warning.format(module_filter))

            plugins = module_plugins
        return plugins

    def _clean_filepath(self, filepath):
        """
        processes the filepath by checking if it is a directory or not
        and adding `.py` if not present.
        """
        if (os.path.isdir(filepath) and
                os.path.isfile(os.path.join(filepath, '__init__.py'))):

            filepath = os.path.join(filepath, '__init__.py')

        if (not filepath.endswith('.py') and
                os.path.isfile(filepath + '.py')):
            filepath += '.py'
        return filepath

    def _processed_filepath(self, filepath):
        """
        checks to see if the filepath has already been processed
        """
        processed = False
        if filepath in self.processed_filepaths.values():
            processed = True

        return processed

    def _update_loaded_modules(self):
        """
        Updates the loaded modules by checking if they are still in sys.modules
        """
        system_modules = sys.modules.keys()
        for module in list(self.loaded_modules):
            if module not in system_modules:
                self.processed_filepaths.pop(module)
                self.loaded_modules.remove(module)
