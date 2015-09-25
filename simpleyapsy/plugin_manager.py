import sys
import os
import itertools

from simpleyapsy import log

class PluginManager(object):
    def __init__(self,
                 plugin_locator=None):

        self.plugin_names_by_type = {}

    def _plugin_names_by_type_helper(self, type_):
        if type_ is None:
            plugin_names = {}
            for value in self.plugin_names_by_type.values():
                plugin_names.update(value)
        elif not isinstance(type_, str):
            # try to find the right string
            key_found = False
            for type_key, klass in self.plugin_classes.items():
                if type_ == klass:
                    break
            else:
                raise
            plugin_names = self.plugin_names_by_type[type_key]
        else:
            plugin_names = self.plugin_names_by_type[type_]
        return plugin_names 

    def get_plugin(self, name, type_=None):
        plugin_names = self._plugin_names_by_type_helper(type_)
        plugin = plugin_names[name]
        return plugin

    def get_plugins(self, type_=None):
        if type_:
            plugin_names = self.plugin_names_by_type[type_]
            plugins = plugin_names.values()
        else:
            # Flattens the list of list returned by self.plugin_names_by_type.values()
            plugins = itertools.chain.from_iterable(self.plugin_names_by_type.values())
        return plugins

    def add_plugin(self, plugin, type_, plugin_info=PluginInfo()):
        dict_ = self.plugin_names_by_type[type_]
        dict_[plugin_info.name] = plugin

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
