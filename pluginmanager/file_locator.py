from simpleyapsy.file_getters import WithInfoFileGetter
from simpleyapsy import util


class FileLocator(object):
    """
    Holds onto and locates the filepaths of plugins using a set of getters
    to determine what files actually corresponds to plugins.
    """
    def __init__(self,
                 file_getters=[WithInfoFileGetter('yapsy-plugin')]):

        file_getters = util.return_list(file_getters)
        self.file_getters = file_getters
        self.plugin_files = set()

    def set_file_getters(self, file_getters):
        file_getters = util.return_list(file_getters)
        self.file_getters = file_getters

    def add_file_getters(self, file_getters):
        file_getters = util.return_list(file_getters)
        self.file_getters.extend(file_getters)

    def locate_filepaths(self, directories):
        """
        Walk through the plugins' places and look for plugins.

        Return the candidates and number of plugins found.
        """
        for directory in directories:
            # Can have more than one file getter
            filepaths = self._file_getter_iterator_helper(directory)
            self.plugin_files.update(filepaths)

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
