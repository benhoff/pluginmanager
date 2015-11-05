from .directory_manager import DirectoryManager
from .file_manager import FileManager
from .module_manager import ModuleManager
from .plugin_manager import PluginManager


class BlacklistInterface(object):
    def __init__(self, **kwargs):
        self.directory_manager = kwargs.get('directory_manager',
                                            DirectoryManager())

        self.file_manager = kwargs.get('file_manager', FileManager())
        self.module_manager = kwargs.get('module_manager', ModuleManager())
        self.plugin_manager = kwargs.get('plugin_manager', PluginManager())

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
