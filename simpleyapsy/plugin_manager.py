import sys
import os
import types
import itertools

from simpleyapsy import log, IPlugin
from simpleyapsy.plugin_getters import SubclassGetter 

class PluginManager(object):
    def __init__(self, 
                 plugin_getters=[SubclassGetter(klass=IPlugin)]):

        self.set_plugin_getters(plugin_getters)
        self.plugins = {}

    def set_plugin_getters(self, plugin_getters):
        if not isinstance(plugin_getters, list):
            plugin_getters = list(plugin_getters)

        self.plugin_getters = plugin_getters

    def add_plugin_getters(self, plugin_getters):
        if not isinstance(plugin_getters, list):
            plugin_getters = list(plugin_getters)

        self.plugin_getters.extend(plugin_getters)

    def get_plugins(self):
        return [x[0] for x in self.plugins.values()]

    def add_plugins(self, plugins, plugin_infos=[]):
        if not isinstance(plugins, list):
            plugins = list(plugins)
        self.plugins.extend(plugins)

    def set_plugins(self, plugins, plugin_infos=[]):
        if not isnstance(plugins, list):
            plugins = list(plugins)
        self.plugins = plugins

    def get_plugin_infos(self):
        return [x[1] for x in self.plugins.values()]

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

    def _plugin_getter_iter_helper(self, module):
        pass

    def _process_plugin(self, plugins, plugin_info=None):
        for plugin in plugins:
            pass
        if plugin_info is None:


    def add_modules(self, modules, plugin_infos=[]):
        if isinstance(modules, dict):
            plugin_infos = modules.values()
            modules = modules.keys()
        if not isinstance(modules, list) and not isinstance(modules, types.GeneratorType):
            modules = list(modules)
        for module, plugin_info in itertools.zip_longest(modules, plugin_infos):
            plugins = self._plugin_getter_iter_helper(module)
            if not plugins == []:
                self._process_plugin(plugins, plugin_info)


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
