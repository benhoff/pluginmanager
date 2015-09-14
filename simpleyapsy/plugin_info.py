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
    def __init__(self, plugin_name, plugin_path):
        self._details = ConfigParser()
        self.name = plugin_name
        self.path = plugin_path
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
