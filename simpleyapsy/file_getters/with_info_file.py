import os
from configparser import ConfigParser

class WithInfoFileGetter(object):
    """
    Only gets files that have configuration files ending with specific extensions
    (nominally 'yapsy-plugin')
    """
    def __init__(self, extensions=["yapsy-plugin"]):
        self.extensions = extensions

    def set_file_extensions(self, extensions):
        self.extensions = extensions

    def add_file_extensions(self, extensions):
        try:
            self.extensions.extend(extensions)
        except TypeError:
            extensions = list(extensions)
            self.extensions.extend(extensions)
            
    def validiate_plugin(self, filename):
        plugin_validated = False
        for extension in self.extensions:
            if filename.endswith(".{}".format(extension)):
                plugin_validated = True
                break

        return plugin_validated
    
    def get_name(self, 
                 infoFileObject, 
                 candidate_infofile=None):
        # parse the information buffer to get info about the plugin
        config_parser = ConfigParser()
        try:
            config_parser.read_file(infoFileObject)
        except Exception:
            return (None, None, None)

        if not config_parser.has_section("Core"):
            return (None, None, None)

        if not config_parser.has_option("Core","Name") or not config_parser.has_option("Core","Module"):
            return (None, None, None)
        # check that the given name is valid

        name = config_parser.get("Core", "Name")
        name = name.strip()
        if PLUGIN_NAME_FORBIDEN_STRING in name:
            return (None, None, None)
        return (name, config_parser.get("Core", "Module"), config_parser)

    def get_files(self, filenames, dir_paths):
        pass
