"""
Role
====

Encapsulate a plugin instance as well as some metadata.

API
===
"""

from configparser import ConfigParser
from distutils.version import StrictVersion


class PluginInfo(object):
    """Representation of the most basic set of information related to a
    given plugin such as its name, author, description...

    Any additional information can be stored ad retrieved in a
    PluginInfo, when this one is created with a
    ``ConfigParser.ConfigParser`` instance.

    This typically means that when metadata is read from a text file
    (the original way for yapsy to describe plugins), all info that is
    not part of the basic variables (name, path, version etc), can
    still be accessed though the ``details`` member variables that
    behaves like Python's ``ConfigParser.ConfigParser``.

    Warning: the instance associated with the ``details`` member
    variable is never copied and used to store all plugin infos. If
    you set it to a custom instance, it will be modified as soon as
    another member variale of the plugin info is
    changed. Alternatively, if you change the instance "outside" the
    plugin info, it will also change the plugin info.

    Ctor Arguments:

            *plugin_name* is  a simple string describing the name of
     the plugin.

            *plugin_path* describe the location where the plugin can be
     found.
            
    .. warning:: The ``path`` attribute is the full path to the
                 plugin if it is organised as a directory or the
                 full path to a file without the ``.py`` extension
                 if the plugin is defined by a simple file. In the
                 later case, the actual plugin is reached via
                 ``plugin_info.path+'.py'``.
    """
    
    def __init__(self, plugin_name, plugin_path):
        self._details = ConfigParser()
        self.name = plugin_name
        self.path = plugin_path
        self._ensureDetailsDefaultsAreBackwardCompatible()
        # Storage for stuff created during the plugin lifetime
        self.plugin_object = None
        self.categories    = []
        self.error = None
   
    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, cfDetails):
        """
        Fill in all details by storing a ``ConfigParser`` instance.

        .. warning: The values for ``plugin_name`` and
                    ``plugin_path`` given a init time will superseed
                    any value found in ``cfDetails`` in section
                    'Core' for the options 'Name' and 'Module' (this
                    is mostly for backward compatibility).
        """	
        bkp_name = self.name
        bkp_path = self.path
        self._details = cfDetails
        self.name = bkp_name
        self.path = bkp_path
        self._ensureDetailsDefaultsAreBackwardCompatible()
    
    @property
    def name(self):
        return self.details.get("Core","Name")
    
    @name.setter
    def name(self, name):
        if not self.details.has_section("Core"):
            self.details.add_section("Core")
        self.details.set("Core","Name",name)

    @property
    def path(self):
        return self.details.get("Core","Module")
    
    @path.setter
    def path(self, path):
        if not self.details.has_section("Core"):
            self.details.add_section("Core")
        self.details.set("Core","Module",path)

    
    @property
    def version(self):
        return StrictVersion(self.details.get("Documentation","Version"))
    
    @version.setter
    def version(self, vstring):
        """
        Set the version of the plugin.

        Used by subclasses to provide different handling of the
        version number.
        """
        if isinstance(vstring,StrictVersion):
            vstring = str(vstring)
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation","Version",vstring)
    
    @property
    def author(self):
        return self.details.get("Documentation","Author")
        
    @author.setter
    def author(self, author):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation","Author",author)

    @property
    def copyright(self):
        return self.details.get("Documentation","Copyright")
    
    @copyright.setter
    def copyright(self, copyrightTxt):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation","Copyright",copyrightTxt)

    @property 
    def website(self):
        return self.details.get("Documentation","Website")
    
    @website.setter
    def website(self, website):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation","Website",website)

    @property 
    def description(self):
        return self.details.get("Documentation","Description")
   
    @description.setter
    def description(self, description):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        return self.details.set("Documentation","Description",description)

    @property
    def category(self):
        """
        DEPRECATED (>1.9): Mimic former behaviour when what is
        noz the first category was considered as the only one the
        plugin belonged to.
        """		
        if self.categories:
            return self.categories[0]
        else:
            return "UnknownCategory"
    
    @category.setter
    def category(self, c):
        """
        DEPRECATED (>1.9): Mimic former behaviour by making so
        that if a category is set as it it was the only category to
        which the plugin belongs, then a __getCategory will return
        this newly set category.
        """
        self.categories = [c] + self.categories
    
    @property
    def is_activated(self):
        """
        Return the activated state of the plugin object.
        Makes it possible to define a property.
        """
        return self.plugin_object.is_activated
    
    def _ensureDetailsDefaultsAreBackwardCompatible(self):
        """
        Internal helper function.
        """
        if not self.details.has_option("Documentation","Author"):
                self.author		= "Unknown"
        if not self.details.has_option("Documentation","Version"):
                self.version	= "0.0"
        if not self.details.has_option("Documentation","Website"):
                self.website	= "None"
        if not self.details.has_option("Documentation","Copyright"):
                self.copyright	= "Unknown"
        if not self.details.has_option("Documentation","Description"):
                self.description = ""
