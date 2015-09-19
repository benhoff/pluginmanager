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
                 directory_list=[],
                 recursive=True):

        if directory_list == []:
            directory_list = [os.path.dirname(__file__)]

        self.directory_list = directory_list
        self.file_getters = file_getters
        self.recursive = recursive 
        self._discovered_plugins = {}
        self._plugin_info_cls_map = {}

    def add_locations(self, paths):
        try:
            self.directory_list.extend(paths)
        except TypeError:
            paths = list(paths)
            self.directory_list.extend(paths)

    def set_locations(self, paths):
        self.directory_list = paths

    def set_file_getters(self, file_getters):
        self.file_getters = file_getters

    def add_file_getters(self, file_getters):
        try:
            self.file_getters.extend(file_getters)
        except TypeError:
            file_getters = list(file_getters)
            self.file_getters.extend(file_getters)
            
    def remove_analyzer_by_param(self, class_name=None, instance_attr=None):
        # FIXME !!
        """
        Removes analyzers of a given name.
        """
        foundAndRemoved = False
        for analyzer in enumerate(self.analyzers):
            if obj.name == name:
                self.analyzers.remove(obj)
                foundAndRemoved = True

    def _register_info_file(self, *args):
        pass

    def _get_dir_iterator(self, directory):
        if self.recursive:
            walk_iter = os.walk(directory, followlinks=True)
        else:
            walk_iter = [(directory, [], os.listdir(directory))]
        return walk_iter

    def _file_getter_helper(self, filenames, dir_path):
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
        for place in map(os.path.abspath, self.plugins_places):
            # check to see if dir
            if os.path.isdir(place):
                walk_iter = self._get_dir_iterator(place)
                # create appropriate walk iterator
                for dir_path, _, filenames in walk_iter:
                    self._analyze_file_helper(filenames, dir_path)
            # FIXME
            else:
                # maybe it is a plugin path
                plugin_path = directory
                self._analyze_file_helper(place)
