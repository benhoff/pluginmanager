import inspect
from pluginmanager import util


class KeywordParser(object):
    def __init__(self, keywords=['PLUGINS']):
        keywords = util.return_list(keywords)
        self.keywords = keywords

    def get_plugins(self, module):
        plugins = []
        module_members = inspect.getmembers(module)

        for name, value in module_members:
            if name in self.keywords:
                plugins.extend(value)

        return plugins
