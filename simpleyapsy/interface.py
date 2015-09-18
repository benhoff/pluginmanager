class Interface(object):
    def __init__(self):
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

    def locate_plugins(self, names=None, klasses=None, categories=None, vesion=None):
        return self.plugin_locator.locate_plugin(namees, klasses, categories, version)

    def get_plugins(self, names=None, klasses=None, categories=None, version=None):
        return self.plugin_manager.get_plugins(names, klasses, categories, version)

    def load_plugins(self, names=None, klasses=None, categories=None, version=None):
        self._loader_changed = True
        return self.plugin_loader.load_plugins(names, klasses, categories, version)

    def get_plugin_infos(self, names=None, klasses=None, categories=None, version=None):
        pass

    def get_active_plugins(self, names=None, klasses=None, categories=None, version=None):
        pass

    def get_active_plugin_names(self, names=None, klasses=None, categories=None, version=None):
        pass

    def activate_plugins(self, names=None, klasses=None, categories=None, version=None):
        pass

    def add_plugins(self, plugin):
        pass
