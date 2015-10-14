import os
from simpleyapsy import util


class FilenameFileGetter(object):
    def __init__(self, filenames=['__init__.py']):
        filenames = util.return_list(filenames)
        self.filenames = filenames

    def plugin_valid(self, filename):
        filename = os.path.basename(filename)
        if filename in self.filenames:
            return True
        return False

    def get_plugin_filepaths(self, dir_path):
        plugin_filepaths = []
        filepaths = util.get_filepaths_from_dir(dir_path)
        for filepath in filepaths:
            if self.plugin_valid(filepath):
                plugin_filepaths.append(filepath)
        return plugin_filepaths
