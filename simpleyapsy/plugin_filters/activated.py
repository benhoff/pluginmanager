def activated(plugins):
    activated = []
    for plugin in plugins:
        if plugin.active:
            activated.append(plugin)

    return activated
