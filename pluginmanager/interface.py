from .file_manager import FileManager
from .plugin_manager import PluginManager
from .module_manager import ModuleManager
from .directory_manager import DirectoryManager


class Interface(object):
    def __init__(self,
                 file_manager=FileManager(),
                 module_manager=ModuleManager(),
                 plugin_manager=PluginManager(),
                 auto_manage_state=True):

        self.managing_state = auto_manage_state
        self.directory_manager = DirectoryManager()
        self.file_manager = file_manager
        self.module_manager = module_manager
        self.plugin_manager = plugin_manager

    def track_site_package_paths(self):
        return self.directory_manager.add_site_packages_paths()

    def collect_plugin_directories(self, directories=None):
        if directories is None:
            directories = self.directory_manager.get_plugin_directories()
        # alias for pep8 reasons
        dir_manage = self.directory_manager
        plugin_directories = dir_manage.collect_plugin_directories(directories)
        return plugin_directories

    def collect_plugin_filepaths(self, directories=None):
        if directories is None:
            directories = self.collect_plugin_directories()
        plugin_filepaths = self.file_manager.collect_filepaths(directories)
        return plugin_filepaths

    def load_modules(self, filepaths=None):
        if filepaths is None:
            filepaths = self.collect_plugin_filepaths()
        loaded_modules = self.module_manager.collect_modules(filepaths)
        return loaded_modules

    def collect_plugins(self, modules=None):
        if modules is None:
            modules = self.load_modules()
        plugins = self.module_manager.collect_plugins(modules)
        if self.managing_state:
            self.add_plugins(plugins)
            self.instantiate_plugins(plugins)
        return plugins

    def reload_modules(self, module_or_module_name):
        self.module_manager.reload_module(module_or_module_name)

    def set_plugins(self, plugins):
        self.plugin_manager.set_plugins(plugins)

    def add_plugins(self, plugins):
        self.plugin_manager.add_plugins(plugins)

    def remove_plugins(self, plugins):
        self.plugin_manager.remove_plugins(plugins)

    def get_plugins(self):
        return self.plugin_manager.get_plugins()

    def blacklist_plugin(self, plugins):
        self.plugin_manager.blacklist_plugins(plugins)

    def configure_plugins(self, config):
        self.plugin_manager.configure_plugins(config)

    def get_configuration_templates(self):
        return self.plugin_manager.get_configuration_templates()

    def check_configurations(self):
        pass

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

    def add_blacklisted_filepaths(self, filepaths):
        self.module_manager.add_blacklisted_filepaths(filepaths)

    def get_blacklisted_filepaths(self):
        return self.module_manager.blacklisted_filepaths

    def set_blacklisted_filepaths(self, filepaths):
        self.module_manager.set_blacklisted_filepaths(filepaths)

    def remove_blacklisted_filepaths(self, filepaths):
        self.module_manager.remove_blacklisted_filepaths(filepaths)

    def add_to_loaded_modules(self, modules):
        self.module_manager.add_to_loaded_modules(modules)

    def get_loaded_modules(self):
        return self.module_manager.get_loaded_modules()

    def add_file_filters(self, file_filters):
        self.file_manager.add_file_filters(file_filters)

    def get_file_filters(self):
        return self.file_manager.file_filters

    def remove_file_filters(self, file_filters):
        self.file_manager.remove_file_filters(file_filters)

    def set_file_filters(self, file_filters):
        self.file_manager.set_file_filters(file_filters)
