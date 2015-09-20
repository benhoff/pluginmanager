import os
import re
import logging

from simpleyapsy import PLUGIN_NAME_FORBIDEN_STRING
from simpleyapsy import log
from simpleyapsy.file_getters import WithInfoFileExt 

class PluginLocator(object):
    """
    Holds onto and locates the filepaths of plugins using a set of getters
    to determine what files actually corresponds to plugins.
    """
    def __init__(self,
                 file_getters=[WithInfoFileExt('yapsy-plugin')],
                 plugin_directories=[],
                 recursive=True):

        if plugin_directories == []:
            plugin_directories = [os.path.dirname(__file__)]

        self.plugin_directories = plugin_directories 
        self.file_getters = file_getters
        self.recursive = recursive
        self.plugin_filepaths = set()

    def add_locations(self, paths):
        try:
            self.plugin_directories.extend(paths)
        except TypeError:
            paths = list(paths)
            self.plugin_directories.extend(paths)

    def set_locations(self, paths):
        self.plugin_directories = paths

    def set_file_getters(self, file_getters):
        self.file_getters = file_getters

    def add_file_getters(self, file_getters):
        try:
            self.file_getters.extend(file_getters)
        except TypeError:
            file_getters = list(file_getters)
            self.file_getters.extend(file_getters)
            
    def remove_analyzer_by_param(self, param_name, param_value):
        """
        Removes analyzers of a given name.
        """
        removed = False
        for getter in self.file_getters:
            if hasattr(getter, param_name) and getattr(getter, param_name) == param_value:
                self.file_getters.remove(getter)
                removed = True
        return removed

    def _get_dir_iterator(self, directory):
        """
        Handles recursion state
        """
        if self.recursive:
            walk_iter = os.walk(directory, followlinks=True)
        else:
            walk_iter = [(directory, [], os.listdir(directory))]
        return walk_iter

    def _file_getter_iterator_helper(self, path):
        """
        helps iterate through all the file getters
        """
        filepaths = []
        info_objects = []
        for getter in self.file_getters:
            plugin_info, plugin_path = getter.get_info_and_filepaths(path)
            # check to see if plugin path is unique, and record if it is
            if not plugin_path in filepaths:
                filepaths.extend(plugin_paths)
                info_objects.extend(plugin_infos)

        return filepaths, info_objects
    
    def locate_plugins(self):
        """
        Walk through the plugins' places and look for plugins.

        Return the candidates and number of plugins found.
        """
        for plugin_directory in map(os.path.abspath, self.plugin_directories):
            # check to see if plugin_directory is a dir
            # otherwise assume it's a plugin path
            if os.path.isdir(plugin_directory):
                # handle whether we're recursively looking through directories
                dir_iter = self._get_dir_iterator(plugin_directory)
                # iterate through the directories
                for dir_path, _, _ in dir_iter:
                    plugin_filepaths, plugin_information = self._file_getter_iterator_helper(dir_path)
                    self.plugin_filepaths.update(plugin_filepaths)

            # otherwise assume it's a plugin path
            else:
                # alias out the path
                plugin_path = plugin_directory
                plugin_filepath, plugin_information = self._file_getter_iterator_helper(plugin_path)
                self.plugin_filepaths.update(plugin_filepath)

        return self.plugin_filepaths
