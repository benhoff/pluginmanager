from .directory_manager import DirectoryManager
from .file_manager import FileManager
from .module_manager import ModuleManager
from .plugin_manager import PluginManager
from .iplugin import IPlugin


class PluginInterface(object):
    def __init__(self, **kwargs):

        self.directory_manager = kwargs.get('directory_manager',
                                            DirectoryManager())

        self.file_manager = kwargs.get('file_manager', FileManager())
        self.module_manager = kwargs.get('module_manager', ModuleManager())
        self.plugin_manager = kwargs.get('plugin_manager', PluginManager())

    def track_site_package_paths(self):
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
        self.directory_manager.add_directories(paths, except_blacklisted)

    def get_plugin_directories(self):
        return self.directory_manager.get_directories()

    def remove_plugin_directories(self, paths):
        self.directory_manager.remove_directories(paths)

    def set_plugin_directories(self, paths, except_blacklisted=True):
        self.directory_manager.set_directories(paths, except_blacklisted)

    def add_plugin_filepaths(self, filepaths):
        self.file_manager.add_plugin_filepaths(filepaths)

    def get_plugin_filepaths(self):
        return self.file_manager.get_plugin_filepaths()

    def remove_plugin_filepaths(self, filepaths):
        self.file_manager.remove_plugin_filepaths(filepaths)

    def set_plugin_filepaths(self, filepaths):
        self.file_manager.set_plugin_filepaths(filepaths)

    def add_to_loaded_modules(self, modules):
        self.module_manager.add_to_loaded_modules(modules)

    def get_loaded_modules(self):
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
        self.file_manager.add_file_filters(file_filters)

    def get_file_filters(self, file_function=None):
        return self.file_manager.get_file_filters(file_function)

    def remove_file_filters(self, file_filters):
        self.file_manager.remove_file_filters(file_filters)

    def set_file_filters(self, file_filters):
        self.file_manager.set_file_filters(file_filters)

    def add_module_plugin_filters(self, module_plugin_filters):
        self.module_manager.add_module_plugin_filters(module_plugin_filters)

    def get_module_plugin_filters(self, filter_function=None):
        return self.module_manager.get_module_plugin_filters(filter_function)

    def remove_module_plugin_filters(self, module_plugin_filters):
        self.module_manager.remove_module_plugin_filters(module_plugin_filters)

    def set_module_plugin_filters(self, module_plugin_filters):
        self.module_manager.set_module_plugin_filters(module_plugin_filters)

    def add_blacklisted_directories(self,
                                    directories,
                                    rm_black_dirs_from_stored_dirs=True):

        add_black_dirs = self.directory_manager.add_blacklisted_directories
        add_black_dirs(directories, rm_black_dirs_from_stored_dirs)

    def get_blacklisted_directories(self):
        return self.directory_manager.get_blacklisted_directories()

    def set_blacklisted_directories(self,
                                    directories,
                                    rm_black_dirs_from_stored_dirs=True):

        set_black_dirs = self.directory_manager.set_blacklisted_directories
        set_black_dirs(directories, rm_black_dirs_from_stored_dirs)

    def remove_blacklisted_directories(self, directories):
        self.directory_manager.remove_blacklisted_directories(directories)

    def add_blacklisted_filepaths(self, filepaths):
        self.file_manager.add_blacklisted_filepaths(filepaths)

    def get_blacklisted_filepaths(self):
        return self.file_manager.get_blacklisted_filepaths()

    def set_blacklisted_filepaths(self, filepaths):
        self.file_manager.set_blacklisted_filepaths(filepaths)

    def remove_blacklisted_filepaths(self, filepaths):
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
