import os
from .compat import getsitepackages

from pluginmanager import util


class DirectoryManager(object):
    def __init__(self,
                 plugin_directories=set(),
                 recursive=True):

        if plugin_directories == set():
            plugin_directories = set()

        self.plugin_directories = plugin_directories
        self.blacklisted_directories = set()
        self.recursive = recursive

    def add_directories(self, paths):
        self.plugin_directories.update(util.return_set(paths))

    def set_directories(self, paths):
        self.plugin_directories = util.return_set(paths)

    def remove_directories(self, paths):
        util.remove_from_set(self.plugin_directories, paths)

    def add_site_packages_paths(self):
        self.add_directories(getsitepackages())

    def add_blacklisted_directories(self, directories):
        self.blacklisted_directories.update(util.return_set(directories))

    def set_blacklisted_directories(self, directories):
        self.blacklisted_directories = util.return_set(directories)

    def get_blacklisted_directories(self):
        return self.blacklisted_directories

    def remove_blacklisted_directories(self, directories):
        util.remove_from_set(self.blacklisted_directories, directories)

    def _remove_blacklisted(self, directories):
        util.remove_from_list(directories, self.blacklisted_directories)
        return directories

    def collect_directories(self, directories):
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

    def get_directories(self):
        self._plugin_dirs_to_absolute_paths()
        return self.plugin_directories

    def _plugin_dirs_to_absolute_paths(self):
        # alias out to meet <80 character line pep req
        abspath = os.path.abspath
        dirs = [abspath(x) for x in self.plugin_directories]
        # casting to set removes dups, casting back to list for type
        self.plugin_directories = util.return_set(dirs)
