import os
import re
import logging

from simpleyapsy import log
from simpleyapsy.file_getters import WithInfoFileGetter

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
        self.plugin_files = {}

    def add_plugin_directories(self, paths):
        unique_paths = set.union(set(paths), set(self.plugin_directories))
        self.plugin_directories = list(unique_paths)

    def set_plugin_directories(self, paths):
        self.plugin_directories = paths

    def set_file_getters(self, file_getters):
        self.file_getters = file_getters

    def add_file_getters(self, file_getters):
        if not isinstance(file_getters, list):
            file_getters = list(file_getters)

        self.file_getters.extend(file_getters)
            
    def remove_getter_by_param(self, param_name, param_value):
        """
        Removes analyzers of a given name.
        """
        removed = False
        for getter in self.file_getters:
            if hasattr(getter, param_name) and getattr(getter, param_name) == param_value:
                self.file_getters.remove(getter)
                removed = True
                break
        return removed

    def locate_files(self):
        """
        Walk through the plugins' places and look for plugins.

        Return the candidates and number of plugins found.
        """
        self._plugin_dirs_to_absolute_paths()

        located_plugin_filepaths = []
        located_plugin_information = [] 

        for plugin_directory in self.plugin_directories:
            # handle whether we're recursively looking through directories
            dir_paths = self._get_dir_iterator(plugin_directory)

            for dir_path in dir_paths:
                # Can have more than one file getter
                filepaths, information = self._file_getter_iterator_helper(dir_path)

                located_plugin_filepaths.extend(filepaths)
                located_plugin_information.extend(information)

        plugin_path_info_tuple = zip(located_plugin_filepaths, located_plugin_information)
        for plugin_path, plugin_info in plugin_path_info_tuple:
            self.plugin_files[plugin_path] = plugin_info

        return self.plugin_files

    def get_plugin_filepaths(self):
        if not self.plugin_files:
            self.locate_plugins()
        return self.plugin_files.keys()

    def _file_getter_iterator_helper(self, path):
        """
        helps iterate through all the file getters
        """
        filepaths = []
        info_objects = []
        for file_getter in self.file_getters:
            plugin_info, plugin_path = file_getter.get_info_and_filepaths(path)

            # check to see if plugin path is unique, and record if it is
            if not plugin_path in filepaths and not plugin_path in self.plugin_files:
                filepaths.extend(plugin_paths)
                info_objects.extend(plugin_infos)

        return filepaths, info_objects

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
        self.plugin_directories = [os.path.abspath(x) for x in self.plugin_directories]
