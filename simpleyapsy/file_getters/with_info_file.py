import os
from configparser import ConfigParser

class InfoFileAnalzyer(object):

    def __init__(self, extension="yapsy-plugin"):
        self.setPluginInfoExtension(extensions)
    
    def setPluginInfoExtension(self,extensions):
        """
        Set the extension that will identify a plugin info file.

        *extensions* May be a string or a tuple of strings if several extensions are expected.
        """
        # Make sure extension is a tuple
        if not isinstance(extensions, tuple):
            extensions = (extensions, )
        self.expectedExtensions = extensions
            
    def isValidPlugin(self, filename):
        """
        Check if it is a valid plugin based on the given plugin info file extension(s).
        If several extensions are provided, the first matching will cause the function
        to exit successfully.
        """
        res = False
        for ext in self.expectedExtensions:
            if filename.endswith(".%s" % ext):
                res = True
                break
        return res
    
    def getPluginNameAndModuleFromStream(self, 
                                         infoFileObject, 
                                         candidate_infofile=None):

        """
        Extract the name and module of a plugin from the
        content of the info file that describes it and which
        is stored in ``infoFileObject``.
        
        .. note:: Prefer using ``_extractCorePluginInfo``
                  instead, whenever possible...
        
        .. warning:: ``infoFileObject`` must be a file-like object:
                     either an opened file for instance or a string
                     buffer wrapped in a StringIO instance as another
                     example.
              
        .. note:: ``candidate_infofile`` must be provided
                  whenever possible to get better error messages.
        
        Return a 3-uple with the name of the plugin, its
        module and the config_parser used to gather the core
        data *in a tuple*, if the required info could be
        localised, else return ``(None,None,None)``.
        
        .. note:: This is supposed to be used internally by subclasses
                      and decorators.
        """
        # parse the information buffer to get info about the plugin
        config_parser = ConfigParser()
        try:
            config_parser.read_file(infoFileObject)
        except Exception as e:
            log.debug("Could not parse the plugin file '%s' (exception raised was '%s')" % (candidate_infofile,e))
            return (None, None, None)
        # check if the basic info is available
        if not config_parser.has_section("Core"):
            log.debug("Plugin info file has no 'Core' section (in '%s')" % candidate_infofile)
            return (None, None, None)
        if not config_parser.has_option("Core","Name") or not config_parser.has_option("Core","Module"):
            log.debug("Plugin info file has no 'Name' or 'Module' section (in '%s')" % candidate_infofile)
            return (None, None, None)
        # check that the given name is valid
        name = config_parser.get("Core", "Name")
        name = name.strip()
        if PLUGIN_NAME_FORBIDEN_STRING in name:
            log.debug("Plugin name contains forbiden character: %s (in '%s')" % (PLUGIN_NAME_FORBIDEN_STRING,
                                                                                                                                                                candidate_infofile))
            return (None, None, None)
        return (name, config_parser.get("Core", "Module"), config_parser)
    
    def _extractCorePluginInfo(self,directory, filename):
        """
        Gather the core information (name, and module to be loaded)
        about a plugin described by it's info file (found at
        'directory/filename').
        
        Return a dictionary with name and path of the plugin as well
        as the ConfigParser instance used to collect these info.
        
        .. note:: This is supposed to be used internally by subclasses
                  and decorators.
        """
        # now we can consider the file as a serious candidate
        if not isinstance(filename, str):
            # filename is a file object: use it
            name, moduleName, config_parser = self.getPluginNameAndModuleFromStream(filename)
        else:
            candidate_infofile_path = os.path.join(directory, filename)
            # parse the information file to get info about the plugin
            with open(candidate_infofile_path) as candidate_infofile:
                name, moduleName, config_parser = self.getPluginNameAndModuleFromStream(candidate_infofile,candidate_infofile_path)
        if (name, moduleName, config_parser) == (None, None, None):
            return (None,None)
        infos = {"name":name, "path":os.path.join(directory, moduleName)}
        return infos, config_parser
    
    def _extractBasicPluginInfo(self,directory, filename):
        """
        Gather some basic documentation about the plugin described by
        it's info file (found at 'directory/filename').
        
        Return a dictionary containing the core information (name and
        path) as well as as the 'documentation' info (version, author,
        description etc).
        
        See also:
        
          ``self._extractCorePluginInfo``
        """
        infos, config_parser = self._extractCorePluginInfo(directory, filename)
        # collect additional (but usually quite usefull) information
        if infos and config_parser and config_parser.has_section("Documentation"):
            if config_parser.has_option("Documentation","Author"):
                infos["author"]	= config_parser.get("Documentation", "Author")
            if config_parser.has_option("Documentation","Version"):
                infos["version"] = config_parser.get("Documentation", "Version")
            if config_parser.has_option("Documentation","Website"):
                infos["website"] = config_parser.get("Documentation", "Website")
            if config_parser.has_option("Documentation","Copyright"):
                infos["copyright"]	= config_parser.get("Documentation", "Copyright")
            if config_parser.has_option("Documentation","Description"):
                infos["description"] = config_parser.get("Documentation", "Description")
        return infos, config_parser
            
    def getInfosDictFromPlugin(self, dirpath, filename):
        """
        Returns the extracted plugin informations as a dictionary.
        This function ensures that "name" and "path" are provided.

        If *callback* function has not been provided for this strategy,
        we use the filename alone to extract minimal informations.
        """
        infos, config_parser = self._extractBasicPluginInfo(dirpath, filename)
        if not infos or infos.get("name", None) is None:
            raise ValueError("Missing *name* of the plugin in extracted infos.")
        if not infos or infos.get("path", None) is None:
            raise ValueError("Missing *path* of the plugin in extracted infos.")
        return infos, config_parser
