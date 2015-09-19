from .plugin_locator import PluginLocator
from .plugin_manager import PluginManager
from .plugin_loader import load_plugin

class Interface(object):
    def __init__(self, auto_manage_state=True):
        self.managing_state = auto_manage_state
        # plugin locator is a container for file analyzers
        self.plugin_locator = None
        self._locator_changed = False

        self.plugin_loader = None
        self._loader_changed = False

        self.plugin_manager = None
        self._manager_changed = False

    def add_plugin_locations(self, paths):
        self._locator_changed = True
        self.plugin_locator.add_locations(paths)

    def set_plugin_locations(self, paths):
        self._locator_changed = True
        self.plugin_locator.set_locations(paths)

    def get_plugin_locations(self):
        return self.plugin_locator.get_locations()

    def locate_plugins(self, 
                       names=None, 
                       klasses=None, 
                       categories=None, 
                       version=None):

        located_plugins = self.plugin_locator.locate_plugin(names, 
                                                            klasses, 
                                                            categories, 
                                                            version)

        return located_plugins

    def get_plugins(self, 
                    names=None, 
                    klasses=None, 
                    categories=None, 
                    version=None):

        plugins = self.plugin_manager.get_plugins(names, 
                klasses, 
                categories, 
                version)

        return plugins

    def load_plugins(self, 
                     names=None, 
                     klasses=None, 
                     categories=None, 
                     version=None):

        loaded_plugins = self.plugin_loader.load_plugins(names, 
                                                         klasses, 
                                                         categories, 
                                                         version)

        return loaded_plugins

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

    def add_plugins(self, plugin):
        pass
