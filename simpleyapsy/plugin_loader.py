import os
import sys
import imp

def _get_unique_module_name(plugin_info):
    plugin_module_name = 'yapsy_loaded_plugin_{name}'.format(plugin_info['name'])
    plugin_module_name += '_{number}'
    for number in range(len(sys.modules)):
        plugin_module_name.format(number)
        if not plugin_module_name in sys.modules:
            break

    return plugin_module_name

def load_plugin(self, plugin_filepaths, plugin_infos):
    """
    returns a list of loaded plugins
    """
    loaded_plugins = []
    for plugin_filepath in plugin_filepaths:
        # Take off `.py` ending if there
        if plugin_filepath.endswith('.py'):
            plugin_filepath = plugin_filepath[:-3]

        if '__init__' in os.path:
            plugin_filepath = os.path.dirname(plugin_filepath)

        plugin_module_name = _get_unique_module_name(plugin_info)

        try:
            if os.path.isdir(plugin_filepath):
