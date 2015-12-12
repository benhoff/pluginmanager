import os
from .compat import getsitepackages

from pluginmanager import util


class DirectoryManager(object):
    def __init__(self,
                 plugin_directories=set(),
                 recursive=True,
                 blacklisted_directories=set()):

        self.plugin_directories = util.return_set(plugin_directories)
        self.blacklisted_directories = util.return_set(blacklisted_directories) 
        self.recursive = recursive

    def collect_directories(self, directories):
        """
        Helper method to return all the directories.

        If `self.recursive` is set to `True` this will iterate through and
        return all of the directories and subdirectories.

        if `self.recursive` is set to `False` this will return the directories
        passed in

        `directories` may be either a single object or an iterable. recommend
        passing in absolute paths instead of relative

        The object returned is a set() object
        """
        directories = util.return_set(directories)

        if not self.recursive:
            return self._remove_blacklisted(directories)

        recursive_dirs = []
        for dir_ in directories:
            walk_iter = os.walk(dir_, followlinks=True)
            walk_iter = [w[0] for w in walk_iter]
            walk_iter = self._remove_blacklisted(walk_iter)
            recursive_dirs.extend(walk_iter)
        return recursive_dirs

    def add_directories(self, paths):
        """
        Add a directory to the plugin directories.

        `paths` may be either a single object or a iterable (with the exception
        of dicts). Paths can be realitve paths but can/will be converted into 
        absolute paths.

        Note that the method `collect_directories` does not natively rely on this
        internal storage when the method is called but must be passed in explicitly
        """
        self.plugin_directories.update(util.return_set(paths))

    def set_directories(self, paths):
        """
        Set the directories. This will delete the previous state stored in 
        `self.plugin_directories

        `paths` may be either a signle object or an iterable (with the exception of
        dict). Paths can be realitve paths but can/will be converted into 
        absolute paths.
        """
        self.plugin_directories = util.return_set(paths)

    def remove_directories(self, paths):
        """
        Removes any paths in the internal storage. Note that depending on how
        the state, somee paths may be relative, some may be absolute. If
        you plan on using this method, recommend that all paths passed to this
        member be passed in as absolute paths for consistency.`

        `paths` may be a single object or an iterable.
        """
        util.remove_from_set(self.plugin_directories, paths)

    def add_site_packages_paths(self):
        """
        A helper method to add all of the site packages tracked by python
        to the directories tracked internally.

        Note that if using a virtualenv there is an outstanding bug with the
        method used here. While there is a hackish workaround, when using a 
        virutalenv this method WILL NOT track every single path tracked by python
        """
        self.add_directories(getsitepackages())

    def add_blacklisted_directories(self, directories):
        """
        Add a directory to be blacklisted. Blacklisted paths will not be returned
        or serached recursively when calling the `collect_directories` method
        
        directories may be a single instance or an iterable. Recommend passing
        in absolute paths
        """
        # TODO: check if blacklisted directories are converted into
        # absolute paths or not?
        self.blacklisted_directories.update(util.return_set(directories))

    def set_blacklisted_directories(self, directories):
        """
        Add a directory to be blacklisted. Blacklisted paths will not be returned
        or serached recursively when calling the `collect_directories` method
        """
        self.blacklisted_directories = util.return_set(directories)

    def get_blacklisted_directories(self):
        return self.blacklisted_directories

    def remove_blacklisted_directories(self, directories):
        util.remove_from_set(self.blacklisted_directories, directories)

    def _remove_blacklisted(self, directories):
        util.remove_from_list(directories, self.blacklisted_directories)
        return directories

    def get_directories(self):
        self._plugin_dirs_to_absolute_paths()
        return self.plugin_directories

    def _plugin_dirs_to_absolute_paths(self):
        # alias out to meet <80 character line pep req
        abspath = os.path.abspath
        dirs = [abspath(x) for x in self.plugin_directories]
        # casting to set removes dups, casting back to list for type
        self.plugin_directories = util.return_set(dirs)
