class PluginManager(object):
    def __init__(self,
                 plugin_filters=[]):

        self.plugins = []
        self.plugin_filters = plugin_filters

    def get_plugins(self):
        return self.plugins

    def add_plugins(self, plugins):
        if not isinstance(plugins, list):
            plugins = list(plugins)
        self.plugins.extend(plugins)

    def set_plugins(self, plugins):
        if not isinstance(plugins, list):
            plugins = list(plugins)
        self.plugins = plugins

    def get_active_plugins(self):
        plugins = self.get_plugins()
        active_plugins = []
        for plugin in plugins:
            if plugin.active:
                active_plugins.append(plugin)
        return active_plugins

    def deactivate_all_plugins(self):
        plugins = self.get_plugins()
        for plugin in plugins:
            plugin.deactivate()
