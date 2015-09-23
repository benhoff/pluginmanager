from .plugin_locator import PluginLocator
from .plugin_manager import PluginManager
from .plugin_loader import load_plugin

class Interface(object):
    def __init__(self, 
                 plugin_locator=PluginLocator(),
                 plugin_manager=PluginManager(),
                 auto_manage_state=True):

        self.managing_state = auto_manage_state
        self.plugin_locator = plugin_locator
        self.plugin_manager = plugin_manager 

    def add_plugin_directories(self, paths):
        self.plugin_locator.add_plugin_directories(paths)

    def set_plugin_locations(self, paths):
        self.plugin_locator.set_plugin_directories(paths)

    def set_file_getters(self, file_getters):
        self.plugin_locator.set_file_getters(file_getters)

    def add_file_getters(self, file_getters):
        self.plugin_locator.add_file_getters(file_getters)

    def remove_file_getter_by_param(self, param_name, param_value):
        self.plugin_locator.remove_getter_by_param(param_name, param_value)

    def get_plugin_locations(self):
        located_plugins = self.plugin_locator.locate_plugin()
        return located_plugins

    def load_plugins(self):
        plugin_locations = self.plugin_locator(names,
                                               klasses, 
                                               categories, 
                                               version)
            
        loaded_plugins = load_plugins(plugin_locations,
                                      names,
                                      klasses,
                                      categories,
                                      version)

        return loaded_plugins

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

    def get_active_plugin_names(self, 
                                names=None, 
                                klasses=None, 
                                categories=None, 
                                version=None):

        active_plugin_names = self.plugin_manager.get_active_plugin_names(
                names,
                klasses,
                categories, 
                version)

        return active_plugin_names

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
