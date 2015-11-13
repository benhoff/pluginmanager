def deactivated(plugins):
    deactivated = []
    for plugin in plugins:
        if hasattr(plugin, 'active') and not plugin.active:
            deactivated.append(plugin)

    return deactivated
