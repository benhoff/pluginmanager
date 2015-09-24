import os
import sys
import inspect
from importlib.machinery import SourceFileLoader

def _get_unique_module_name(plugin_info):
    plugin_module_name = 'yapsy_loaded_plugin_{name}'.format(plugin_info['name'])
    plugin_module_name += '_{number}'
    for number in range(len(sys.modules)):
        plugin_module_name.format(number)
        if not plugin_module_name in sys.modules:
            break

    return plugin_module_name

class PluginLoader(object):
    def __init__(self):
        self.loaded_plugins = []
        self.blacklisted_plugin_filepaths = []

    def blacklist_plugin(self, filepath):
        self.blacklisted_plugin_filepaths.append(filepath)

    def load_plugin(self, plugin_locations, plugin_infos=None):
        """
        returns a list of loaded plugins
        """
        loaded_plugins = []
        for plugin_filepath in plugin_filepaths:
            if plugin_filepath in self.blacklisted_plugin_filepaths:
                break

            # Take off `.py` ending if there
            if plugin_filepath.endswith('.py'):
                plugin_filepath = plugin_filepath[:-3]
            
            # NOTE: think actually want to ADD __init__.py as plugin filepath
            if '__init__' in os.path.basename(plugin_filepath)
                plugin_filepath = os.path.dirname(plugin_filepath)

            plugin_module_name = _get_unique_module_name(plugin_info)

            try:
                if os.path.isdir(plugin_filepath):
                    # TODO: source file loader cannot take in a directory
                    pass
                module = SourceFileLoader(plugin_module_name, plugin_filepath)
                for attribute in dir(module):
                    # FIXME
                    if inspect.isclass(attribute):
                        loaded_plugins.append(attribute())




    return loaded_plugins
