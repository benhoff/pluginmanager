from pluginmanager import util


class KeywordParser(object):
    def __init__(self, keywords=['PLUGINS']):
        keywords = util.return_list(keywords)
        self.keywords = keywords

    def __call__(self, plugins, names):
        for plugin, name in zip(plugins, names):
            if name not in self.keywords:
                plugins.remove(plugin)
        return plugins
