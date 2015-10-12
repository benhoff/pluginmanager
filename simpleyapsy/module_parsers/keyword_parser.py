import inspect


class KeywordParser(object):
    def __init__(self, keywords=['plugins']):
        self.keywords = keywords

    def get_plugins(self, module):
        plugins = []
        module_members = inspect.getmembers(module)

        for name, value in module_members:
            if name in self.keywords:
                plugins.append(value)

        return plugins
