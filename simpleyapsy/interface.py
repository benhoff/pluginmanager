from .file_locator import FileLocator
from .plugin_manager import PluginManager
from .module_loader import ModuleLoader


class Interface(object):
    def __init__(self,
                 file_locator=FileLocator(),
                 module_loader=ModuleLoader(),
                 plugin_manager=PluginManager(),
                 auto_manage_state=True):

        self.managing_state = auto_manage_state
        self.file_locator = file_locator
        self.module_loader = module_loader
        self.plugin_manager = plugin_manager

    def add_plugin_directories(self, paths):
        self.file_locator.add_plugin_directories(paths)

    def set_plugin_locations(self, paths):
        self.file_locator.set_plugin_directories(paths)

    def set_file_getters(self, file_getters):
        self.file_locator.set_file_getters(file_getters)

    def add_file_getters(self, file_getters):
        self.file_locator.add_file_getters(file_getters)

    def remove_file_getter_by_param(self, param_name, param_value):
        self.file_locator.remove_getter_by_param(param_name, param_value)

    def get_plugin_locations(self):
        located_plugins = self.file_locator.locate_plugins()
        return located_plugins

    def blacklist_filepaths(self, filepaths):
        self.module_loader.blacklist_filepaths(filepaths)

    def set_blacklisted_filepaths(self, filepaths):
        self.module_loader.set_blacklisted_filepaths(filepaths)

    def get_blacklisted_filepaths(self):
        return self.module_loader.blacklisted_filepaths

    def load_modules(self, filepaths=None):
        if filepaths is None:
            filepaths = self.file_locator.get_plugin_filepaths()

        self.module_loader.load_modules(filepaths)
        if self.managing_state:
            modules = self.module_loader.get_loaded_modules()
            self.plugin_manager.add_modules(modules)

    def reload_modules(self, module_or_module_name):
        self.module_loader.reload_module(module_or_module_name)

    def get_plugins(self,
                    names=None,
                    klasses=None,
                    categories=None,
                    version=None):

        if self.managing_state:
            loaded_plugins = self.load_plugins(names,
                                               klasses,
                                               categories,
                                               version)

            self.plugin_manager.set_plugins(loaded_plugins)

        plugins = self.plugin_manager.get_plugins(names,
                                                  klasses,
                                                  categories,
                                                  version)

        return plugins

    def get_plugin_infos(self,
                         names=None,
                         klasses=None,
                         categories=None,
                         version=None):

        pass

    def get_active_plugins(self,
                           names=None,
                           klasses=None,
                           categories=None,
                           version=None):

        active_plugins = self.plugin_manager.get_active_plugins(names,
                                                                klasses,
                                                                categories,
                                                                version)

        return active_plugins

    def activate_plugins(self,
                         names=None,
                         klasses=None,
                         categories=None,
                         version=None):

        self.plugin_manager.activate_plugins(names,
                                             klasses,
                                             categories,
                                             version)

    def set_plugins(self, plugin):
        if self.managing_state:
            pass
