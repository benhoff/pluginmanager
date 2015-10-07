def deactived(plugins):
    deactivated = []
    for pluign in plugins:
        if not plugin.active:
            deactivated.append(plugin)

    return deactivated
