def deactivated(plugins):
    deactivated = []
    for plugin in plugins:
        if not plugin.active:
            deactivated.append(plugin)

    return deactivated
