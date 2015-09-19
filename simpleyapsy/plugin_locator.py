import os
import re
import logging

from simpleyapsy import PLUGIN_NAME_FORBIDEN_STRING
from simpleyapsy import log
from simpleyapsy.file_getters import WithInfoFileExt 

class PluginLocator(object):
    """
    Locates plugins on the file system using a set of analyzers to
    determine what files actually corresponds to plugins.
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
        self._discovered_plugins = {}

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
            
    def remove_analyzer_by_param(self, class_name=None):
        """
        Removes analyzers of a given name.
        """
        removed = False
        for analyzer in enumerate(self.analyzers):
            if analyzer.name == name:
                self.analyzers.remove(obj)
                removed = True
        return removed

    def _register_info_file(self, *args):
        pass

    def _get_dir_iterator(self, directory):
        if self.recursive:
            walk_iter = os.walk(directory, followlinks=True)
        else:
            walk_iter = [(directory, [], os.listdir(directory))]
        return walk_iter

    def _file_getter_helper(self, filenames, dir_path):
        """
        helps parse through all the file getters
        """
        files = []
        for getter in self.file_getters:
            candidate_files = getter.get_files(filenames, dir_path)
            files.extend(candidate_files)
        return files
    
    def locate_plugins(self, 
                       names=None, 
                       klasses=None, 
                       categories=None, 
                       version=None):

        """
        Walk through the plugins' places and look for plugins.

        Return the candidates and number of plugins found.
        """
        for place in map(os.path.abspath, self.plugin_directories):
            # check to see if dir
            if os.path.isdir(place):
                walk_iter = self._get_dir_iterator(place)
                # create appropriate walk iterator
                for dir_path, _, filenames in walk_iter:
                    files = self._file_getter_helper(filenames, dir_path)
            # FIXME
            else:
                # maybe it is a plugin path
                plugin_path = directory
                self._analyze_file_helper(place)
