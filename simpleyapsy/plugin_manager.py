from simpleyapsy import util


class PluginManager(object):
    def __init__(self):
        self.plugins = []
        self.blacklisted_plugins = []

    def get_plugins(self):
        return self.plugins

    def blacklist_plugins(self, plugins):
        self.blacklisted_plugins.extend(plugins)

    def add_plugins(self, plugins):
        plugins = util.return_list(plugins)
        for plugin in plugins:
            if plugin not in self.blacklisted_plugins:
                self.plugins.append(plugin)

    def set_plugins(self, plugins):
        plugins = util.return_list(plugins)
        self.plugins = []

        for plugin in plugins:
            if plugin not in self.blacklisted_plugins:
                self.plugins.append(plugin)
