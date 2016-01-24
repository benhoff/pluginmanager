import os
from .compat import getsitepackages

from pluginmanager import util


class DirectoryManager(object):
    """
    `DirectoryManager` manages the recursive search state and can
    optionally manage directory state. The default implementation of
    pluginmanager uses `DirectoryManager` to manage the directory state.

    `DirectoryManager` contains a directory blacklist, which can be used to
    stop from collecting from uninteresting directories.

    `DirectoryManager` manages directory state through the add/get/set
    directories methods.

    NOTE: When calling `collect_directories` the directories must be
    explicitly passed into the method call. This is to avoid tight coupling
    from the internal state and promote reuse at the Interface level.
    """
    def __init__(self,
                 plugin_directories=None,
                 recursive=True,
                 blacklisted_directories=None):
        """
        `recursive` is used to control whether directories are searched
        recursviely or not

        `plugin_directories` may be a single directories or an iterable.

        `blacklisted_directories` may be a single directory or an iterable
        """

        self.recursive = recursive
        self.plugin_directories = None
        self.blacklisted_directories = None
        if plugin_directories is None:
            plugin_directories = set()
        if blacklisted_directories is None:
            blacklisted_directories = set()

        self.set_directories(plugin_directories)
        self.set_blacklisted_directories(blacklisted_directories)

    def collect_directories(self, directories):
        """
        Collects all the directories into a `set` object.

        If `self.recursive` is set to `True` this method will iterate through
        and return all of the directories and the subdirectories found from
        `directories` that are not blacklisted.

        if `self.recursive` is set to `False` this will return all the
        directories that are not balcklisted.

        `directories` may be either a single object or an iterable. Recommend
        passing in absolute paths instead of relative. `collect_directories`
        will attempt to convert `directories` to absolute paths if they are not
        already.
        """
        directories = util.to_absolute_paths(directories)

        if not self.recursive:
            return self._remove_blacklisted(directories)

        recursive_dirs = set()
        for dir_ in directories:
            walk_iter = os.walk(dir_, followlinks=True)
            walk_iter = [w[0] for w in walk_iter]
            walk_iter = util.to_absolute_paths(walk_iter)
            walk_iter = self._remove_blacklisted(walk_iter)
            recursive_dirs.update(walk_iter)
        return recursive_dirs

    def add_directories(self, directories, except_blacklisted=True):
        """
        Adds `directories` to the set of plugin directories.

        `directories` may be either a single object or a iterable.

        `directories` can be relative paths, but will be converted into
        absolute paths based on the current working directory.

        if `except_blacklisted` is `True` all `directories` in
        `self.blacklisted_directories` will be removed
        """
        directories = util.to_absolute_paths(directories)
        if except_blacklisted:
            directories = self._remove_blacklisted(directories)

        self.plugin_directories.update(directories)

    def set_directories(self, directories, except_blacklisted=True):
        """
        Sets the plugin directories to `directories`. This will delete
        the previous state stored in `self.plugin_directories` in favor
        of the `directories` passed in.

        `directories` may be either a single object or an iterable.

        `directories` can contain relative paths but will be
        converted into absolute paths based on the current working
        directory.

        if `except_blacklisted` is `True` all `directories` in
        `self.blacklisted_directories` will be removed
        """
        directories = util.to_absolute_paths(directories)
        if except_blacklisted:
            directories = self._remove_blacklisted(directories)

        self.plugin_directories = directories

    def remove_directories(self, directories):
        """
        Removes any `directories` from the set of plugin directories.

        `directories` may be a single object or an iterable.

        Recommend passing in all paths as absolute, but the method will
        attemmpt to convert all paths to absolute if they are not already
        based on the current working directory.
        """
        directories = util.to_absolute_paths(directories)
        self.plugin_directories = util.remove_from_set(self.plugin_directories,
                                                       directories)

    def add_site_packages_paths(self):
        """
        A helper method to add all of the site packages tracked by python
        to the set of plugin directories.

        NOTE that if using a virtualenv, there is an outstanding bug with the
        method used here. While there is a workaround implemented, when using a
        virutalenv this method WILL NOT track every single path tracked by
        python. See: https://github.com/pypa/virtualenv/issues/355
        """
        site_packages = getsitepackages()
        self.add_directories(site_packages)

    def add_blacklisted_directories(self,
                                    directories,
                                    remove_from_stored_directories=True):

        """
        Adds `directories` to be blacklisted. Blacklisted directories will not
        be returned or searched recursively when calling the
        `collect_directories` method.

        `directories` may be a single instance or an iterable. Recommend
        passing in absolute paths, but method will try to convert to absolute
        paths based on the current working directory.

        If `remove_from_stored_directories` is true, all `directories`
        will be removed from `self.plugin_directories`
        """
        absolute_paths = util.to_absolute_paths(directories)
        self.blacklisted_directories.update(absolute_paths)
        if remove_from_stored_directories:
            plug_dirs = self.plugin_directories
            plug_dirs = util.remove_from_set(plug_dirs,
                                             directories)

    def set_blacklisted_directories(self,
                                    directories,
                                    remove_from_stored_directories=True):
        """
        Sets the `directories` to be blacklisted. Blacklisted directories will
        not be returned or searched recursively when calling
        `collect_directories`.

        This will replace the previously stored set of blacklisted
        paths.

        `directories` may be a single instance or an iterable. Recommend
        passing in absolute paths. Method will try to convert to absolute path
        based on current working directory.
        """
        absolute_paths = util.to_absolute_paths(directories)
        self.blacklisted_directories = absolute_paths
        if remove_from_stored_directories:
            plug_dirs = self.plugin_directories
            plug_dirs = util.remove_from_set(plug_dirs,
                                             directories)

    def get_blacklisted_directories(self):
        """
        Returns the set of the blacklisted directories.
        """
        return self.blacklisted_directories

    def remove_blacklisted_directories(self, directories):
        """
        Attempts to remove the `directories` from the set of blacklisted
        directories. If a particular directory is not found in the set of
        blacklisted, method will continue on silently.

        `directories` may be a single instance or an iterable. Recommend
        passing in absolute paths. Method will try to convert to an absolute
        path if it is not already using the current working directory.
        """
        directories = util.to_absolute_paths(directories)
        black_dirs = self.blacklisted_directories
        black_dirs = util.remove_from_set(black_dirs, directories)

    def _remove_blacklisted(self, directories):
        """
        Attempts to remove the blacklisted directories from `directories`
        and then returns whatever is left in the set.

        Called from the `collect_directories` method.
        """
        directories = util.to_absolute_paths(directories)
        directories = util.remove_from_set(directories,
                                           self.blacklisted_directories)

        return directories

    def get_directories(self):
        """
        Returns the plugin directories in a `set` object
        """
        return self.plugin_directories
