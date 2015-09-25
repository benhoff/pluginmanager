import logging
log = logging.getLogger('simpleyapsy')

PLUGIN_NAME_FORBIDEN_STRING=";;"

# TODO: move
def NormalizePluginNameForModuleName(pluginName):
    """
    Normalize a plugin name into a safer name for a module name.
    
    .. note:: may do a little more modifications than strictly
              necessary and is not optimized for speed.
    """
    if len(pluginName)==0:
        return "_"
    if pluginName[0].isdigit():
        pluginName = "_" + pluginName
    ret = RE_NON_ALPHANUM.sub("_",pluginName)
    return ret

import re
from .iplugin import IPlugin
from .plugin_locator import PluginLocator
from .plugin_manager import PluginManager

RE_NON_ALPHANUM = re.compile("\W")
