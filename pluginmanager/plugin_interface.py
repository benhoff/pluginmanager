from .directory_manager import DirectoryManager
from .file_manager import FileManager
from .module_manager import ModuleManager
from .entry_point_manager import EntryPointManager
from .plugin_manager import PluginManager
from .iplugin import IPlugin


class PluginInterface(object):
    def __init__(self, **kwargs):

        self.directory_manager = kwargs.get('directory_manager',
                                            DirectoryManager())

        self.file_manager = kwargs.get('file_manager', FileManager())
        self.module_manager = kwargs.get('module_manager', ModuleManager())
        self.entry_point_manager = kwargs.get('entry_point_manager',
                                              EntryPointManager())

        self.plugin_manager = kwargs.get('plugin_manager', PluginManager())

    def track_site_package_paths(self):
        """
        A helper method to add all of the site packages tracked by python
        to the set of plugin directories.

        NOTE that if using a virtualenv, there is an outstanding bug with the
        method used here. While there is a workaround implemented, when using a
        virutalenv this method WILL NOT track every single path tracked by
        python. See: https://github.com/pypa/virtualenv/issues/355
        """
        return self.directory_manager.add_site_packages_paths()

    def collect_plugin_directories(self, directories=None):
        if directories is None:
            directories = self.get_plugin_directories()
        # alias for pep8 reasons
        dir_manage = self.directory_manager
        plugin_directories = dir_manage.collect_directories(directories)
        return plugin_directories

    def collect_plugin_filepaths(self, directories=None):
        if directories is None:
            directories = self.collect_plugin_directories()
        plugin_filepaths = self.file_manager.collect_filepaths(directories)
        return plugin_filepaths

    def load_modules(self, filepaths=None):
        if filepaths is None:
            filepaths = self.collect_plugin_filepaths()
        loaded_modules = self.module_manager.load_modules(filepaths)
        return loaded_modules

    def collect_plugins(self,
                        modules=None,
                        store_collected_plugins=True):

        if modules is None:
            modules = self.load_modules()
        plugins = self.module_manager.collect_plugins(modules)
        if store_collected_plugins:
            self.add_plugins(plugins)
        return plugins

    def collect_entry_point_plugins(self,
                                    entry_point_names=None,
                                    verify_requirements=False,
                                    store_collected_plugins=True,
                                    return_dict=False):

        collect_plugins = self.entry_point_manager.collect_plugins
        plugins = collect_plugins(entry_point_names,
                                  verify_requirements,
                                  return_dict)

        if store_collected_plugins:
            if return_dict:
                self.plugin_manager.plugins.extend(plugins.values())
            else:
                self.plugin_manager.plugins.extend(plugins)

        return plugins

    def set_plugins(self, plugins):
        """
        sets plugins to the internal state.
        If the instance member `instantiate_classes` in the underlying
        member `plugin_manager` is True and the plugins
        have class instances in them, attempts to instatiate the classes.
        The default is `True`

        This can be checked/changed by:

            `plugin_interface.plugin_manager.instantiate_classes`

        If the instance member `unique_instances` in the underlying member
        `plugin_manager` is True and duplicate instances are passed in,
        this method will not track the new instances internally.
        The default is `True`

        This can be checked/changed by:

            `plugin_interface.plugin_manager.unique_instances`

        """
        self.plugin_manager.set_plugins(plugins)

    def add_plugins(self, plugins):
        """
        Adds plugins to the internal state. `plugins` may be a single
        object or an iterable.

        If the instance member `instantiate_classes` in the underlying
        member `plugin_manager` is True and the plugins
        have class instances in them, attempts to instatiate the classes.
        Default is `True`

        This can be checked/changed by:

            `plugin_interface.plugin_manager.instantiate_classes`

        If the instance member `unique_instances` in the underlying member
        `plugin_manager` is True and duplicate instances are passed in,
        this method will not track the new instances internally.
        Default is `True`

        This can be checked/changed by:

            `plugin_interface.plugin_manager.unique_instances`

        """
        self.plugin_manager.add_plugins(plugins)

    def remove_plugins(self, plugins):
        """
        removes `plugins` from the internal state

        `plugins` may be a single object or an iterable.
        """
        self.plugin_manager.remove_plugins(plugins)

    def get_plugins(self, filter_function=None):
        """
        Gets out the plugins from the internal state. Returns a list
        object.

        If the optional filter_function is supplied, applies the filter
        function to the arguments before returning them. Filters should
        be callable and take a list argument of plugins.
        """
        return self.plugin_manager.get_plugins(filter_function)

    def add_plugin_directories(self, paths, except_blacklisted=True):
        """
        Adds `directories` to the set of plugin directories.

        `directories` may be either a single object or a iterable.

        `directories` can be relative paths, but will be converted into
        absolute paths based on the current working directory.

        if `except_blacklisted` is `True` all `directories` in
        that are blacklisted will be removed
        """
        self.directory_manager.add_directories(paths, except_blacklisted)

    def get_plugin_directories(self):
        """
        Returns the plugin directories in a `set` object
        """
        return self.directory_manager.get_directories()

    def remove_plugin_directories(self, paths):
        """
        Removes any `directories` from the set of plugin directories.

        `directories` may be a single object or an iterable.

        Recommend passing in all paths as absolute, but the method will
        attemmpt to convert all paths to absolute if they are not already
        based on the current working directory.
        """
        self.directory_manager.remove_directories(paths)

    def set_plugin_directories(self, paths, except_blacklisted=True):
        """
        Sets the plugin directories to `directories`. This will delete
        the previous state stored in `self.plugin_directories` in favor
        of the `directories` passed in.

        `directories` may be either a single object or an iterable.

        `directories` can contain relative paths but will be
        converted into absolute paths based on the current working
        directory.

        if `except_blacklisted` is `True` all `directories` in
        blacklisted that are blacklisted will be removed
        """
        self.directory_manager.set_directories(paths, except_blacklisted)

    def add_entry_points(self, names):
        self.entry_point_manager.add_entry_points(names)

    def remove_entry_points(self, names):
        self.entry_point_manager.remove_entry_points(names)

    def set_entry_points(self, names):
        self.entry_point_manager.set_entry_points(names)

    def get_entry_points(self):
        return self.entry_point_manager.get_entry_points()

    def add_plugin_filepaths(self, filepaths, except_blacklisted=True):
        """
        Adds `filepaths` to internal state. Recommend passing
        in absolute filepaths. Method will attempt to convert to
        absolute paths if they are not already.

        `filepaths` can be a single object or an iterable

        If `except_blacklisted` is `True`, all `filepaths` that
        have been blacklisted will not be added.
        """
        self.file_manager.add_plugin_filepaths(filepaths,
                                               except_blacklisted)

    def get_plugin_filepaths(self):
        """
        returns the plugin filepaths tracked internally as a `set` object.
        """
        return self.file_manager.get_plugin_filepaths()

    def remove_plugin_filepaths(self, filepaths):
        """
        Removes `filepaths` from internal state.
        Recommend passing in absolute filepaths. Method will
        attempt to convert to absolute paths if not passed in.

        `filepaths` can be a single object or an iterable.
        """
        self.file_manager.remove_plugin_filepaths(filepaths)

    def set_plugin_filepaths(self, filepaths, except_blacklisted=True):
        """
        Sets internal state to `filepaths`. Recommend passing
        in absolute filepaths. Method will attempt to convert to
        absolute paths if they are not already.

        `filepaths` can be a single object or an iterable.

        If `except_blacklisted` is `True`, all `filepaths` that
        have been blacklisted will not be set.
        """
        self.file_manager.set_plugin_filepaths(filepaths,
                                               except_blacklisted)

    def add_to_loaded_modules(self, modules):
        """
        Manually add in `modules` to be tracked by the module manager.

        `modules` may be a single object or an iterable.
        """
        self.module_manager.add_to_loaded_modules(modules)

    def get_loaded_modules(self):
        """
        Returns all modules loaded by this instance.
        """
        return self.module_manager.get_loaded_modules()

    def get_instances(self, filter_function=IPlugin):
        """
        Gets instances out of the internal state using
        the default filter supplied in filter_function.
        By default, it is the class IPlugin.

        Can optionally pass in a list or tuple of classes
        in for `filter_function` which will accomplish
        the same goal.

        lastly, a callable can be passed in, however
        it is up to the user to determine if the
        objects are instances or not.
        """
        return self.plugin_manager.get_instances(filter_function)

    def add_file_filters(self, file_filters):
        """
        Adds `file_filters` to the internal file filters.
        `file_filters` can be single object or iterable.
        """
        self.file_manager.add_file_filters(file_filters)

    def get_file_filters(self, filter_function=None):
        """
        Gets the file filters.
        `filter_function`, can be a user defined filter. Should be callable
        and return a list.
        """
        return self.file_manager.get_file_filters(filter_function)

    def remove_file_filters(self, file_filters):
        """
        Removes the `file_filters` from the internal state.
        `file_filters` can be a single object or an iterable.
        """
        self.file_manager.remove_file_filters(file_filters)

    def set_file_filters(self, file_filters):
        """
        Sets internal file filters to `file_filters` by tossing old state.
        `file_filters` can be single object or iterable.
        """
        self.file_manager.set_file_filters(file_filters)

    def add_module_plugin_filters(self, module_plugin_filters):
        """
        Adds `module_plugin_filters` to the internal module filters.
        May be a single object or an iterable.

        Every module filters must be a callable and take in
        a list of plugins and their associated names.
        """
        self.module_manager.add_module_plugin_filters(module_plugin_filters)

    def get_module_plugin_filters(self, filter_function=None):
        """
        Gets the internal module filters. Returns a list object.

        If supplied, the `filter_function` should take in a single
        list argument and return back a list. `filter_function` is
        designed to given the option for a custom filter on the module filters.
        """
        return self.module_manager.get_module_plugin_filters(filter_function)

    def remove_module_plugin_filters(self, module_plugin_filters):
        """
        Removes `module_plugin_filters` from the internal module filters.
        If the filters are not found in the internal representation,
        the function passes on silently.

        `module_plugin_filters` may be a single object or an iterable.
        """
        self.module_manager.remove_module_plugin_filters(module_plugin_filters)

    def set_module_plugin_filters(self, module_plugin_filters):
        """
        Sets the internal module filters to `module_plugin_filters`
        `module_plugin_filters` may be a single object or an iterable.

        Every module filters must be a callable and take in
        a list of plugins and their associated names.
        """
        self.module_manager.set_module_plugin_filters(module_plugin_filters)

    def add_blacklisted_directories(self,
                                    directories,
                                    rm_black_dirs_from_stored_dirs=True):
        """
        Adds `directories` to be blacklisted. Blacklisted directories will not
        be returned or searched recursively when calling the
        `collect_directories` method.

        `directories` may be a single instance or an iterable. Recommend
        passing in absolute paths, but method will try to convert to absolute
        paths based on the current working directory.

        If `remove_from_stored_directories` is true, all `directories`
        will be removed from internal state.
        """
        add_black_dirs = self.directory_manager.add_blacklisted_directories
        add_black_dirs(directories, rm_black_dirs_from_stored_dirs)

    def get_blacklisted_directories(self):
        """
        Returns the set of the blacklisted directories.
        """
        return self.directory_manager.get_blacklisted_directories()

    def set_blacklisted_directories(self,
                                    directories,
                                    rm_black_dirs_from_stored_dirs=True):
        """
        Sets the `directories` to be blacklisted. Blacklisted directories will
        not be returned or searched recursively when calling
        `collect_directories`.

        This will replace the previously stored set of blacklisted
        paths.

        `directories` may be a single instance or an iterable. Recommend
        passing in absolute paths. Method will try to convert to absolute path
        based on current working directory.
        """
        set_black_dirs = self.directory_manager.set_blacklisted_directories
        set_black_dirs(directories, rm_black_dirs_from_stored_dirs)

    def remove_blacklisted_directories(self, directories):
        """
        Attempts to remove the `directories` from the set of blacklisted
        directories. If a particular directory is not found in the set of
        blacklisted, method will continue on silently.

        `directories` may be a single instance or an iterable. Recommend
        passing in absolute paths. Method will try to convert to an absolute
        path if it is not already using the current working directory.
        """
        self.directory_manager.remove_blacklisted_directories(directories)

    def add_blacklisted_filepaths(self, filepaths, remove_from_stored=True):
        """
        Add `filepaths` to blacklisted filepaths.
        If `remove_from_stored` is `True`, any `filepaths` in
        internal state will be automatically removed.
        """
        self.file_manager.add_blacklisted_filepaths(filepaths,
                                                    remove_from_stored)

    def get_blacklisted_filepaths(self):
        """
        Returns the blacklisted filepaths as a set object.
        """
        return self.file_manager.get_blacklisted_filepaths()

    def set_blacklisted_filepaths(self, filepaths, remove_from_stored=True):
        """
        Sets internal blacklisted filepaths to filepaths.
        If `remove_from_stored` is `True`, any `filepaths` in
        internal state will be automatically removed.
        """
        self.file_manager.set_blacklisted_filepaths(filepaths)

    def remove_blacklisted_filepaths(self, filepaths):
        """
        Removes `filepaths` from blacklisted filepaths.
        `filepaths` may be a single filepath or iterable of filepaths.
        recommend passing in absolute filepaths but method will attempt
        to convert to absolute filepaths based on current working directory.
        """
        self.file_manager.remove_blacklisted_filepaths(filepaths)

    def add_blacklisted_plugins(self, plugins):
        """
        add blacklisted plugins.
        `plugins` may be a single object or iterable.
        """
        self.plugin_manager.add_blacklisted_plugins(plugins)

    def get_blacklisted_plugins(self):
        """
        gets blacklisted plugins tracked in the internal state
        Returns a list object.
        """
        return self.plugin_manager.get_blacklisted_plugins()

    def set_blacklisted_plugins(self, plugins):
        """
        sets blacklisted plugins.
        `plugins` may be a single object or iterable.
        """
        self.plugin_manager.set_blacklisted_plugins(plugins)

    def remove_blacklisted_plugins(self, plugins):
        """
        removes `plugins` from the blacklisted plugins.
        `plugins` may be a single object or iterable.
        """
        self.plugin_manager.remove_blacklisted_plugins(plugins)
