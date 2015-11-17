from .directory_manager import DirectoryManager
from .file_manager import FileManager
from .module_manager import ModuleManager
from .plugin_manager import PluginManager
from .iplugin import IPlugin


class PluginInterface(object):
    def __init__(self,
                 auto_manage_state=True,
                 **kwargs):

        self.managing_state = auto_manage_state
        self.directory_manager = kwargs.get('directory_manager',
                                            DirectoryManager())

        self.file_manager = kwargs.get('file_manager', FileManager())
        self.module_manager = kwargs.get('module_manager', ModuleManager())
        self.plugin_manager = kwargs.get('plugin_manager', PluginManager())
        self._managers = {'directory_manager': self.directory_manager,
                          'file_manager': self.file_manager,
                          'module_manager': self.module_manager,
                          'plugin_manager': self.plugin_manager}

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

    def collect_plugins(self, modules=None):
        if modules is None:
            modules = self.load_modules()
        plugins = self.module_manager.collect_plugins(modules)
        if self.managing_state:
            self.add_plugins(plugins)
        return plugins

    def set_plugins(self, plugins):
        self.plugin_manager.set_plugins(plugins)

    def add_plugins(self, plugins):
        self.plugin_manager.add_plugins(plugins)

    def remove_plugins(self, plugins):
        self.plugin_manager.remove_plugins(plugins)

    def get_plugins(self, filter_function=None):
        return self.plugin_manager.get_plugins(filter_function)

    def add_plugin_directories(self, paths):
        self.directory_manager.add_directories(paths)

    def get_plugin_directories(self):
        return self.directory_manager.get_directories()

    def remove_plugin_directories(self, paths):
        self.directory_manager.remove_directories(paths)

    def set_plugin_directories(self, paths):
        self.directory_manager.set_directories(paths)

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
        return self.plugin_manager.get_instances(filter_function)

    def add_file_filters(self, file_filters):
        self.file_manager.add_file_filters(file_filters)

    def get_file_filters(self, file_function=None):
        return self.file_manager.get_file_filters(file_function)

    def remove_file_filters(self, file_filters):
        self.file_manager.remove_file_filters(file_filters)

    def set_file_filters(self, file_filters):
        self.file_manager.set_file_filters(file_filters)

    def add_module_filters(self, module_filters):
        self.module_manager.add_module_filters(module_filters)

    def get_module_filters(self, filter_function=None):
        return self.module_manager.get_module_filters(filter_function)

    def remove_module_filters(self, module_filters):
        self.module_manager.remove_module_filters(module_filters)

    def set_module_filters(self, module_filters):
        self.module_manager.set_module_filters(module_filters)

    def add_blacklisted_directories(self, directories):
        self.directory_manager.add_blacklisted_directories(directories)

    def get_blacklisted_directories(self):
        return self.directory_manager.get_blacklisted_directories()

    def set_blacklisted_directories(self, directories):
        self.directory_manager.set_blacklisted_directories(directories)

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
        self.plugin_manager.add_blacklisted_plugins(plugins)

    def get_blacklisted_plugins(self):
        return self.plugin_manager.get_blacklisted_plugins()

    def set_blacklisted_plugins(self, plugins):
        self.plugin_manager.set_blacklisted_plugins(plugins)

    def remove_blacklisted_plugins(self, plugins):
        self.plugin_manager.remove_blacklisted_plugins(plugins)
