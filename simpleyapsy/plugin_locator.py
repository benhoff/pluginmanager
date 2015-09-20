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
            
    def remove_analyzer_by_param(self, name, value):
        """
        Removes analyzers of a given name.
        """
        removed = False
        for getter in self.file_getters:
            if hasattr(getter, name) and getattr(getter, name) == value:
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

    def _file_getter_helper(self, path):
        """
        helps parse through all the file getters
        """
        filepaths = []
        for getter in self.file_getters:
            plugin_infos, plugin_paths = getter.get_info_and_filepaths(path)
            filepaths.extend(found_filepaths)
        return filepaths 
    
    def locate_plugins(self):
        """
        Walk through the plugins' places and look for plugins.

        Return the candidates and number of plugins found.
        """
        for plugin_directory in map(os.path.abspath, self.plugin_directories):
            # check to see if dir
            # else assume it's directly a plugin path
            if os.path.isdir(plugin_directory):
                dir_iter = self._get_dir_iterator(plugin_directory)
                # create appropriate walk iterator
                for dir_path, _, _ in dir_iter:
                    plugin_filepaths = self._file_getter_helper(dir_path)
                    self.plugin_filepaths.update(plugin_filepaths)
            else:
                # alias out the path
                plugin_path = plugin_directory 
                plugin_filepath = self._file_getter_helper(plugin_path)
                self.plugin_filepaths.update(plugin_filepath)

        return self.plugin_filepaths
