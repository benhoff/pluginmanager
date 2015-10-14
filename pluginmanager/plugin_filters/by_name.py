from simpleyapsy import util


def by_name(plugins, names):
    names = util.return_list(names)
    approved_plugins = []
    for plugin in plugins:
        if plugin.name in names:
            approved_plugins.append(plugin)

    return approved_plugins
