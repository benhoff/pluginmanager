from simpleyapsy.iplugin import IPlugin
import inspect


class SubclassParser(object):
    def __init__(self, klass=IPlugin):
        self.klass = klass

    def get_plugins(self, module):
        plugins = []
        module_members = inspect.getmembers(module)

        # NOTE: `name` unused here but left for documentation
        for name, value in module_members:
            if issubclass(value, self.klass) and not value == IPlugin:
                plugins.append(value)

        return plugins
