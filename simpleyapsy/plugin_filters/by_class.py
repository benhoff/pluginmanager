def by_class(plugins, classes):
    approved_plugins = []
    for plugin in plugins:
        if isinstance(plugin, classes):
            approved_plugins.append(plugin)

    return approved_plugins
