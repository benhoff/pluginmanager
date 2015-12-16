from pluginmanager import util


class NameFilter(object):
    def __init__(self, names=None):
        if names is None:
            names = []
        self.names = util.return_list(names)

    def __call__(self, plugins):
        approved_plugins = []
        for plugin in plugins:
            if hasattr(plugin, 'name') and plugin.name in self.names:
                approved_plugins.append(plugin)
        return approved_plugins
