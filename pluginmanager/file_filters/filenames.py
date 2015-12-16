import os
from pluginmanager import util


class FilenameFileFilter(object):
    def __init__(self, filenames='__init__.py'):
        filenames = util.return_list(filenames)
        self.filenames = filenames

    def __call__(self, filepaths):
        plugin_filepaths = []
        for filepath in filepaths:
            if self.plugin_valid(filepath):
                plugin_filepaths.append(filepath)
        return plugin_filepaths

    def plugin_valid(self, filename):
        filename = os.path.basename(filename)
        if filename in self.filenames:
            return True
        return False
