from .plugin_locator import PluginLocator
from .plugin_manager import PluginManager
from .plugin_loader import load_plugin

class Interface(object):
    def __init__(self, auto_manage_state=True):
        self.managing_state = auto_manage_state
        # plugin locator is a container for file analyzers
        self.plugin_locator = None
        self.plugin_loader = None
        self.plugin_manager = None

    def add_plugin_locations(self, paths):
        self.plugin_locator.add_locations(paths)
        if self.managing_state:
            self.get_plugins()

    def set_plugin_locations(self, paths):
        # TODO: think about unloading plugins here?
        self.plugin_locator.set_locations(paths)
        if self.managing_state:
            self.get_plugins()

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

        if self.managing_state:
            # TODO: don't load plugins if no state has changed?
            loaded_plugins = self.load_plugins(names, klasses, categories, version)
            self.plugin_manager.set_plugins(loaded_plugins)

        plugins = self.plugin_manager.get_plugins(names, 
                klasses, 
                categories, 
                version)

        return plugins

    def load_plugins(self, 
                     locations=None,
                     names=None, 
                     klasses=None, 
                     categories=None, 
                     version=None):

        if self.managing_state:
            state_locations = self.plugin_locator.locate_plugins(names, 
                                            klasses, 
                                            categories, 
                                            version)

            if locations is not None:
                locations.extend(state_locations)
            else:
                locations = state_locations
            
        loaded_plugins = load_plugins(locations,
                                      names,
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

    def set_plugins(self, plugin):
        if self.managing_state:
            pass
