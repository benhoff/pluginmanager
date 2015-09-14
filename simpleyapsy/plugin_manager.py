import sys
import os
import imp

from simpleyapsy import log
from simpleyapsy import NormalizePluginNameForModuleName

from simpleyapsy import IPlugin
from simpleyapsy import PluginFileLocator
from simpleyapsy import PLUGIN_NAME_FORBIDEN_STRING
from simpleyapsy import PluginInfo

class PluginManager(object):
    def __init__(self,
                 plugin_types={'default':IPlugin},
                 file_manager=None):

        self.plugin_types = plugin_types
        self.file_manager = file_manager

        # Duck type the list on for ease of access
        self.plugin_directories = self.file_manager.plugin_directories

        self.setCategoriesFilter(categories_filter)
        self.setPluginLocator(plugin_locator, directories_list)

    def get_plugins(self, type=None):
        pass

    def get_types(self):
        """
        Return the list of all categories.
        """
        return list(self.plugin_types.keys())

    def removePluginFromCategory(self, plugin,category_name):
        """
        Remove a plugin from the category where it's assumed to belong.
        """
        self.category_mapping[category_name].remove(plugin)


    def appendPluginToCategory(self, plugin, category_name):
        """
        Append a new plugin to the given category.
        """
        self.category_mapping[category_name].append(plugin)

    def getPluginCandidates(self):
        """
        Return the list of possible plugins.

        Each possible plugin (ie a candidate) is described by a 3-uple:
        (info file path, python file path, plugin info instance)

        .. warning: locatePlugins must be called before !
        """
        if not hasattr(self, '_candidates'):
            raise RuntimeError("locatePlugins must be called before getPluginCandidates")
        return self._candidates[:]

    def removePluginCandidate(self,candidateTuple):
        """
        Remove a given candidate from the list of plugins that should be loaded.

        The candidate must be represented by the same tuple described
        in ``getPluginCandidates``.

        .. warning: locatePlugins must be called before !
        """
        if not hasattr(self, '_candidates'):
            raise ValueError("locatePlugins must be called before removePluginCandidate")
        self._candidates.remove(candidateTuple)

    def locatePlugins(self):
        """
        Convenience method (actually call the IPluginLocator method)
        """
        self._candidates, npc = self.getPluginLocator().locatePlugins()
    
    def loadPlugins(self, callback=None):
        """
        Load the candidate plugins that have been identified through a
        previous call to locatePlugins.  For each plugin candidate
        look for its category, load it and store it in the appropriate
        slot of the ``category_mapping``.

        If a callback function is specified, call it before every load
        attempt.  The ``plugin_info`` instance is passed as an argument to
        the callback.
        """
# 		print "%s.loadPlugins" % self.__class__
        if not hasattr(self, '_candidates'):
            raise ValueError("locatePlugins must be called before loadPlugins")

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

    def getPluginByName(self,name,category="Default"):
        """
        Get the plugin correspoding to a given category and name
        """
        if category in self.category_mapping:
            for item in self.category_mapping[category]:
                if item.name == name:
                    return item
        return None

    def activatePluginByName(self,name,category="Default"):
        """
        Activate a plugin corresponding to a given category + name.
        """
        pta_item = self.getPluginByName(name,category)
        if pta_item is not None:
            plugin_to_activate = pta_item.plugin_object
            if plugin_to_activate is not None:
                log.debug("Activating plugin: %s.%s"% (category,name))
                plugin_to_activate.activate()
                return plugin_to_activate			
        return None

    def deactivatePluginByName(self,name,category="Default"):
        """
        Desactivate a plugin corresponding to a given category + name.
        """
        if category in self.category_mapping:
            plugin_to_deactivate = None
            for item in self.category_mapping[category]:
                if item.name == name:
                    plugin_to_deactivate = item.plugin_object
                    break
            if plugin_to_deactivate is not None:
                log.debug("Deactivating plugin: %s.%s"% (category,name))
                plugin_to_deactivate.deactivate()
                return plugin_to_deactivate			
        return None
