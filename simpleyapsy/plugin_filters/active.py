def active(plugins):
    activated = []
    for pluign in plugins:
        if plugin.active:
            activated.append(plugin)
    
    return activated
