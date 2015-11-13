from .directory_manager import DirectoryManager
from .file_manager import FileManager
from .module_manager import ModuleManager
from .plugin_manager import PluginManager


class FilterInterface(object):
    def __init__(self, **kwargs):
        self.directory_manager = kwargs.get('directory_manager',
                                            DirectoryManager())

        self.file_manager = kwargs.get('file_manager', FileManager())
        self.module_manager = kwargs.get('module_manager', ModuleManager())
        self.plugin_manager = kwargs.get('plugin_manager', PluginManager())

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
