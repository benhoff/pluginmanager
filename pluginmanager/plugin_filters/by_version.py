def by_version(plugins, max_version=None, min_version=None):
    min_approved_plugins = []
    max_approved_plugins = []
    for plugin in plugins:
        if plugin.version is None:
            continue
        if min_version and plugin.version >= min_version:
            min_approved_plugins.append(plugin)

        if max_version and plugin.version <= max_version:
            max_approved_plugins.append(plugin)

    if max_approved_plugins and min_approved_plugins:
        pass
    elif (max_version and min_version and not
            max_approved_plugins and not
            min_approved_plugins):

        return []

    elif max_approved_plugins:
        return max_approved_plugins
    else:
        return min_approved_plugins
