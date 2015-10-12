import os
try:
    from site import getsitepackages
except ImportError:
    # getsitepackages is broken with virtualenvs
    # https://github.com/pypa/virtualenv/issues/355
    from distutils.sysconfig import get_python_lib as getsitepackages

from simpleyapsy import util


class DirectoryManager(object):
    def __init__(self,
                 plugin_directories=set(),
                 recursive=True):

        if plugin_directories == set():
            plugin_directories = set()
            plugin_directories.add(os.path.dirname(__file__))

        self.plugin_directories = plugin_directories
        self.recursive = recursive

    def add_directories(self, paths):
        paths = util.return_list(paths)
        unique_paths = set.union(set(paths), set(self.plugin_directories))
        self.plugin_directories = unique_paths

    def set_directories(self, paths):
        paths = util.return_list(paths)
        self.plugin_directories = set(paths)

    def add_site_packages_paths(self):
        self.add_directories(getsitepackages())

    def get_directories(self):
        self._plugin_dirs_to_absolute_paths()
        if not self.recursive:
            return self.plugin_directories
        # TODO: CLEANUP
        recursive_dirs = []
        for dir in self.plugin_directories:
            walk_iter = os.walk(dir, followlinks=True)
            walk_iter = [w[0] for w in walk_iter]
            recursive_dirs.extend(walk_iter)
        return recursive_dirs

    def _plugin_dirs_to_absolute_paths(self):
        # alias out to meet <80 character line pep req
        abspath = os.path.abspath
        self.plugin_directories = [abspath(x) for x in self.plugin_directories]
        # casting to set removes dups, casting back to list for type
        self.plugin_directories = set(self.plugin_directories)
