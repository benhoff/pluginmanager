import inspect
from pluginmanager import util
from pluginmanager.iplugin import IPlugin


class SubclassParser(object):
    def __init__(self, klass=IPlugin):
        self.klass = tuple(util.return_list(klass))

    def __call__(self, plugins, *args):
        result = []
        for plugin in plugins:
            if inspect.isclass(plugin) and issubclass(plugin, self.klass):
                result.append(plugin)
        return result
