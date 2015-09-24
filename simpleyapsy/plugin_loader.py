import os
import sys
import inspect
from importlib.machinery import SourceFileLoader
from simpleyapsy import plugin_validators

def _get_unique_module_name(plugin_info):
    plugin_module_name = 'yapsy_loaded_plugin_{name}'.format(plugin_info['name'])
    plugin_module_name += '_{number}'
    for number in range(len(sys.modules)):
        plugin_module_name.format(number)
        if not plugin_module_name in sys.modules:
            break

    return plugin_module_name

class PluginLoader(object):
    def __init__(self,
                 module_parser=plugin_validators.IsSubclass()):
        self.loaded_plugins = []
        self.processed_filepaths = []
        self.blacklisted_filepaths = []
        self.module_parser = module_parser

    def blacklist_plugin(self, filepath):
        self.blacklisted_filepaths.append(filepath)

    def get_blacklisted_filepaths(self):
        return self.blacklisted_filepaths

    def load_plugin(self, plugin_locations, plugin_infos=None):
        """
        returns a list of loaded plugins
        """
        for plugin_filepath in plugin_filepaths:
            if plugin_filepath in self.blacklisted_filepaths or plugin_filepath in self.processed_filepaths:
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
                self.processed_filepaths.append(plugin_filepath)
                for attribute in dir(module):
                    attribute = getattr(module, attribute)
                    if self.module_parser.is_valid(attribute):
                        self.loaded_plugins.append(attribute)

            except Exception:
                pass

    return self.loaded_plugins
