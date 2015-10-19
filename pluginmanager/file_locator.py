from pluginmanager import util


class FileLocator(object):
    """
    Holds onto and locates the filepaths of plugins using a set of getters
    to determine what files actually corresponds to plugins.
    """
    def __init__(self,
                 filepath_parsers=[]):

        filepath_parsers = util.return_list(filepath_parsers)
        self.filepath_parsers = filepath_parsers
        self.plugin_files = set()

    def add_plugin_filepaths(self, filepaths):
        filepaths = set(util.return_list(filepaths))
        self.plugin_files.update(filepaths)

    def set_plugin_filepaths(self, filepaths):
        filepaths = set(util.return_list(filepaths))
        self.plugin_files = filepaths

    def set_filepath_parsers(self, filepath_parsers):
        filepath_parsers = util.return_list(filepath_parsers)
        self.filepath_parsers = filepath_parsers

    def add_file_parsers(self, filepath_parsers):
        filepath_parsers = util.return_list(filepath_parsers)
        self.filepath_parsers.extend(filepath_parsers)

    def collect_filepaths(self, directories):
        """
        Walk through the plugins' places and look for plugins.

        Return the candidates and number of plugins found.
        """
        plugin_files = set()
        directories = util.return_list(directories)
        for directory in directories:
            filepaths = util.get_filepaths_from_dir(directory)
            filepaths = self._filter_filepaths(directory)
            plugin_files.update(filepaths)

        return plugin_files

    def get_plugin_filepaths(self):
        return self.plugin_files

    def _filter_filepaths(self, filepaths):
        """
        helps iterate through all the file parsers
        """
        if self.filepath_parsers:
            plugin_files = set()
            for filepath_parser in self.filepath_parsers:
                plugin_paths = filepath_parsers.filter_filepaths(filepaths)
                plugin_files.update(plugin_paths)
            filepaths = plugin_files

        return filepaths
