from simpleyapsy import util


def by_class(plugins, classes):
    classes = util.return_list(classes)
    approved_plugins = []
    for plugin in plugins:
        for klass in classes:
            if isinstance(plugin, klass):
                approved_plugins.append(plugin)
                break

    return approved_plugins
