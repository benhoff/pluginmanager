import os
import re
import logging
from configparser import ConfigParser

from simpleyapsy import PluginInfo
from simpleyapsy import PLUGIN_NAME_FORBIDEN_STRING
from simpleyapsy import log
from simpleyapsy.file_getters import WithInfoFileExt 

class PluginLocator(object):
    """
    Locates plugins on the file system using a set of analyzers to
    determine what files actually corresponds to plugins.
    
    If more than one analyzer is being used, the first that will discover a
    new plugin will avoid other strategies to find it too.

    By default each directory set as a "plugin place" is scanned
    recursively. You can change that by a call to
    ``disableRecursiveScan``.
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
        self._max_size = 1e3*1024 # in octets (by default 1 Mo)
            
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

    def _analyze_file_helper(self, filenames, dir_path):
        for analyzer in self.analyzers:
            candidate_files = analyzer.analyze_files(filenames, dir_path)
            self._register_info_file(candidate_files)
    
    def locate(self):
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
