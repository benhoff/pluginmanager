import os
from .compat import getsitepackages

from pluginmanager import util


def _to_absolute_paths(paths):
    """
    helper method to change paths to absolute paths. Returns a `set` object
    `paths` can be either an object or iterable
    """
    abspath = os.path.abspath
    paths = util.return_set(paths)
    absolute_paths = {abspath(x) for x in paths}
    return absolute_paths


class DirectoryManager(object):
    """
    `DirectoryManager` manages whether to recursively search through the
    directories or not when collecting directories and can optionally manage
    directory state. The default implementation of pluginmanager uses the
    internal data storage of `DirectoryManager` to manage the directory state.

    `DirectoryManager` contains a directory blacklist, which can be used to
    stop from including undesirable or uninteresting directories.

    Directory manager can also be used to track directories through the
    add/get/set directories methods.

    NOTE: When calling `collect_directories`, the directories tracked
    internally must be explicitly passed into the method call. This is to
    avoid tight coupling and promote reuse at the Interface level.
    """
    def __init__(self,
                 plugin_directories=set(),
                 recursive=True,
                 blacklisted_directories=set()):

        self.plugin_directories = util.return_set(plugin_directories)
        blacklisted_dirs = blacklisted_directories
        self.blacklisted_directories = util.return_set(blacklisted_dirs)
        self.recursive = recursive

    def collect_directories(self, directories):
        """
        Method to return all the directories in a `set` object

        If `self.recursive` is set to `True` this method will iterate through
        and return all of the directories and the subdirectories found from the
        argument `directories`.

        if `self.recursive` is set to `False` this will return the directories
        passed in after converting them to a set

        `directories` may be either a single object or an iterable. Recommend
        passing in absolute paths instead of relative.
        """
        directories = _to_absolute_paths(directories)

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
        of dicts). Paths can be realitve paths but will be converted into
        absolute paths.

        Note that the method `collect_directories` does not natively rely on
        this internal storage when the method is called but must be passed in
        explicitly.
        """
        self.plugin_directories.update(_to_absolute_paths(paths))

    def set_directories(self, paths):
        """
        Set the directories. This will delete the previous state stored in
        `self.plugin_directories` in favor of the `paths` object passed in.

        `paths` may be either a signle object or an iterable (with the
        exception of dict). Paths can be realitve paths but will be
        converted into absolute paths.
        """
        self.plugin_directories = _to_absolute_paths(paths)

    def remove_directories(self, paths):
        """
        Removes any paths in the internal storage. Recommend passing in all
        paths as absolute, but the method will attemmpt to convert on it's own.

        `paths` may be a single object or an iterable.
        """
        paths = _to_absolute_paths(paths)
        util.remove_from_set(self.plugin_directories, paths)

    def add_site_packages_paths(self):
        """
        A helper method to add all of the site packages tracked by python
        to the set of directories tracked internally.

        NOTE that if using a virtualenv, there is an outstanding bug with the
        method used here. While there is a workaround implemented, when using a
        virutalenv this method WILL NOT track every single path tracked by
        python.
        """
        self.add_directories(getsitepackages())

    def add_blacklisted_directories(self, directories):
        """
        Add a directory to be blacklisted. Blacklisted paths will not be
        returned or serached recursively when calling the `collect_directories`
        method.

        directories may be a single instance or an iterable. Recommend passing
        in absolute paths, but method will try to convert to absolute paths.
        """
        absolute_paths = _to_absolute_paths(directories)
        self.blacklisted_directories.update(absolute_paths)

    def set_blacklisted_directories(self, directories):
        """
        Add a directory to be blacklisted. Blacklisted paths will not be
        returned or serached recursively when calling the `collect_directories`
        method. This will replace the previously stored set of blacklisted
        paths.

        `directories` may be a single instance or an iterable. Recommend
        passing in absolute paths. Method will try to convert to absolute path.
        """
        absolute_paths = _to_absolute_paths(directories)
        self.blacklisted_directories = util.return_set(absolute_paths)

    def get_blacklisted_directories(self):
        """
        Returns a set of the blacklisted directories
        """
        return self.blacklisted_directories

    def remove_blacklisted_directories(self, directories):
        directories = _to_absolute_paths(directories)
        util.remove_from_set(self.blacklisted_directories, directories)

    def _remove_blacklisted(self, directories):
        directories = _to_absolute_paths(directories)
        util.remove_from_set(directories, self.blacklisted_directories)
        return directories

    def get_directories(self):
        return self.plugin_directories
