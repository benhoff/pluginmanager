import sys
import os
import imp
import itertools

from simpleyapsy import log
from simpleyapsy import NormalizePluginNameForModuleName

from simpleyapsy import IPlugin
from simpleyapsy import PluginFileLocator
from simpleyapsy import PLUGIN_NAME_FORBIDEN_STRING
from simpleyapsy import PluginInfo

class PluginManager(object):
    def __init__(self,
                 plugin_classes={'default': IPlugin},
                 plugin_locator=None):

        self.plugin_classes = plugin_classes
        self.plugin_locator = plugin_locator
        self.plugin_names_by_type = {}

        for type_ in self.plugin_classes.keys():
            self.plugin_names_by_type[type_] = {}

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

    def reload_plugin(self, name, type_=None):
        pass

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

    def locatePlugins(self):
        self._candidates, npc = self.getPluginLocator().locatePlugins()
    
    def unload_plugin(self, name, type_=None):
        pass

    def load_plugins(self, callback=None):
        processed_plugins = []
        for candidate_infofile, candidate_filepath, plugin_info in self._candidates:
            # make sure to attribute a unique module name to the one
            # that is about to be loaded
            plugin_module_name_template = NormalizePluginNameForModuleName("yapsy_loaded_plugin_" + plugin_info.name) + "_%d"
            for plugin_name_suffix in range(len(sys.modules)):
                plugin_module_name =  plugin_module_name_template % plugin_name_suffix
                if plugin_module_name not in sys.modules:
                    break
                
                # tolerance on the presence (or not) of the py extensions
                if candidate_filepath.endswith(".py"):
                    candidate_filepath = candidate_filepath[:-3]
                # if a callback exists, call it before attempting to load
                # the plugin so that a message can be displayed to the
                # user
                if callback is not None:
                    callback(plugin_info)
                # cover the case when the __init__ of a package has been
                # explicitely indicated
                if "__init__" in  os.path.basename(candidate_filepath):
                    candidate_filepath = os.path.dirname(candidate_filepath)
                try:
                    # use imp to correctly load the plugin as a module
                    if os.path.isdir(candidate_filepath):
                        candidate_module = imp.load_module(plugin_module_name,None,candidate_filepath,("py","r",imp.PKG_DIRECTORY))
                    else:
                        with open(candidate_filepath+".py","r") as plugin_file:
                            candidate_module = imp.load_module(plugin_module_name,plugin_file,candidate_filepath+".py",("py","r",imp.PY_SOURCE))
                except Exception:
                    exc_info = sys.exc_info()
                    log.error("Unable to import plugin: %s" % candidate_filepath, exc_info=exc_info)
                    plugin_info.error = exc_info
                    processed_plugins.append(plugin_info)
                    continue
                processed_plugins.append(plugin_info)
                if "__init__" in  os.path.basename(candidate_filepath):
                    sys.path.remove(plugin_info.path)
                # now try to find and initialise the first subclass of the correct plugin interface
                for element in (getattr(candidate_module,name) for name in dir(candidate_module)):
                    plugin_info_reference = None
                    for category_name in self.categories_interfaces:
                        try:
                            is_correct_subclass = issubclass(element, self.categories_interfaces[category_name])
                        except Exception:
                            continue
                        if is_correct_subclass and element is not self.categories_interfaces[category_name]:
                            current_category = category_name
                            if candidate_infofile not in self._category_file_mapping[current_category]:
                                    # we found a new plugin: initialise it and search for the next one
                                if not plugin_info_reference:
                                    try:
                                        plugin_info.plugin_object = self.instanciateElement(element)
                                        plugin_info_reference = plugin_info
                                    except Exception:
                                        exc_info = sys.exc_info()
                                        log.error("Unable to create plugin object: %s" % candidate_filepath, exc_info=exc_info)
                                        plugin_info.error = exc_info
                                        break # If it didn't work once it wont again
                                plugin_info.categories.append(current_category)
                                self.category_mapping[current_category].append(plugin_info_reference)
                                self._category_file_mapping[current_category].append(candidate_infofile)
        # Remove candidates list since we don't need them any more and
        # don't need to take up the space
        delattr(self, '_candidates')
        return processed_plugins

    def collectPlugins(self):
        """
        Walk through the plugins' places and look for plugins.  Then
        for each plugin candidate look for its category, load it and
        stores it in the appropriate slot of the category_mapping.
        """
        self.locatePlugins()
        self.loadPlugins()
