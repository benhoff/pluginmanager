import os
import site

from simpleyapsy.file_getters import WithInfoFileGetter
from simpleyapsy import util


class FileLocator(object):
    """
    Holds onto and locates the filepaths of plugins using a set of getters
    to determine what files actually corresponds to plugins.
    """
    def __init__(self,
                 file_getters=[WithInfoFileGetter('yapsy-plugin')],
                 plugin_directories=[],
                 recursive=True):

        if plugin_directories == []:
            plugin_directories = [os.path.dirname(__file__)]

        self.plugin_directories = plugin_directories
        self.file_getters = file_getters
        self.recursive = recursive
        self.plugin_files = set()

    def add_plugin_directories(self, paths):
        paths = util.return_list(paths)
        unique_paths = set.union(set(paths), set(self.plugin_directories))
        self.plugin_directories = list(unique_paths)

    def set_plugin_directories(self, paths):
        paths = util.return_list(paths)
        self.plugin_directories = paths

    def add_site_packages_paths(self):
        self.add_plugin_directories(site.getsitepackages())

    def set_file_getters(self, file_getters):
        file_getters = util.return_list(file_getters)
        self.file_getters = file_getters

    def add_file_getters(self, file_getters):
        file_getters = util.return_list(file_getters)
        self.file_getters.extend(file_getters)

    def locate_filepaths(self, directories=None):
        """
        Walk through the plugins' places and look for plugins.

        Return the candidates and number of plugins found.
        """
        self._plugin_dirs_to_absolute_paths()
        for plugin_directory in self.plugin_directories:
            # handle whether we're recursively looking through directories
            dir_paths = self._get_dir_iterator(plugin_directory)

            for dir_path in dir_paths:
                # Can have more than one file getter
                filepaths = self._file_getter_iterator_helper(dir_path)
                self.plugin_files.add(filepaths)

        return self.plugin_files

    def get_plugin_filepaths(self):
        return self.plugin_files

    def _file_getter_iterator_helper(self, dir_path):
        """
        helps iterate through all the file getters
        """
        filepaths = set()
        for file_getter in self.file_getters:
            plugin_paths = file_getter.get_plugin_filepaths(dir_path)
            filepaths.update(plugin_paths)

        return filepaths

    def _get_dir_iterator(self, directory):
        """
        Handles recursion
        """
        if self.recursive:
            walk_iter = os.walk(directory, followlinks=True)
            walk_iter = [w[0] for w in walk_iter]
        else:
            walk_iter = [directory]
        return walk_iter

    def _plugin_dirs_to_absolute_paths(self):
        # alias out to meet <80 character line pep req
        abspath = os.path.abspath
        self.plugin_directories = [abspath(x) for x in self.plugin_directories]
        # casting to set removes dups, casting back to list for type
        self.plugin_directories = list(set(self.plugin_directories))
