import sys
import os
import itertools

from simpleyapsy import log, IPlugin
from simpleyapsy.plugin_getters import SubclassGetter 

class PluginManager(object):
    def __init__(self, 
                 plugin_getters=[SubclassGetter(klass=IPlugin)]):

        self.plugin_getters = plugin_getters
        self.plugins = []

    def set_plugin_getters(self, plugin_getters):
        if not isinstance(plugin_getters, list):
            plugin_getters = list(plugin_getters)

        self.plugin_getters = plugin_getters

    def add_plugin_getters(self, plugin_getters):
        if not isinstance(plugin_getters, list):
            plugin_getters = list(plugin_getters)

        self.plugin_getters.extend(plugin_getters)

    def get_plugins(self, type_=None):
        if type_:
            plugin_names = self.plugin_names_by_type[type_]
            plugins = plugin_names.values()
        else:
            # Flattens the list of list returned by self.plugin_names_by_type.values()
            plugins = itertools.chain.from_iterable(self.plugin_names_by_type.values())
        return plugins

    def add_plugins(self, plugins):
        if not isinstance(plugins, list):
            plugins = list(plugins)
        self.plugins.extend(plugins)

    def set_plugins(self, plugins):
        if not isnstance(plugins, list):
            plugins = list(plugins)
        self.plugins = plugins

    def get_plugin_info(self, name, type_=None):
        pass

    def get_plugins_infos(self, type_=None):
        pass

    def deactivate_plugin(self, name, type_=None):
        plugin = self.get_plugin(name, type_)
        plugin.deactivate()

    def get_active_plugins(self, type_=None):
        plugins = self.get_plugins(type_)
        active_plugins = []
        for plugin in plugins:
            if plugin.active:
                active_plugins.append(plugin)
        return active_plugins

    def add_modules(self, modules):
        if not isinstance(modules, list):
            modules = list(modules)

        for plugin_getter in self.plugin_getters:
            pass


    def get_active_plugin_names(self, type_=None):
        pass

    def deactivate_all_plugins(self):
        plugins = self.get_plugins()
        for plugin in plugins:
            plugin.deactivate()

    def get_plugin_types(self):
        """
        Return the list of all categories.
        """
        return list(self.plugin_classes.keys())
