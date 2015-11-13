def activated(plugins):
    activated = []
    for plugin in plugins:
        if hasattr(plugin, 'active') and plugin.active:
            activated.append(plugin)

    return activated
