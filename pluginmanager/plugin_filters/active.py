class ActiveFilter(object):
    def __init__(self, active=True):
        self.active = active

    def __call__(self, plugins):
        activated = []
        for plugin in plugins:
            if hasattr(plugin, 'active') and plugin.active == self.active:
                activated.append(plugin)

        return activated
