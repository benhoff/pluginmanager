from pluginmanager import util


class FileManager(object):
    """
    Holds onto and locates the filepaths of plugins using a set of getters
    to determine what files actually corresponds to plugins.
    """
    def __init__(self,
                 file_filters=[]):

        file_filters = util.return_list(file_filters)
        self.file_filters = file_filters
        self.plugin_files = set()
        self.blacklisted_filepaths = set()

    def add_plugin_filepaths(self, filepaths):
        filepaths = set(util.return_list(filepaths))
        self.plugin_files.update(filepaths)

    def set_plugin_filepaths(self, filepaths):
        filepaths = set(util.return_list(filepaths))
        self.plugin_files = filepaths

    def remove_plugin_filepaths(self, filepaths):
        filepaths = set(util.return_list(filepaths))
        for filepath in filepaths:
            if filepath in self.plugin_files:
                self.plugin_files.remove(filepath)

    def set_file_filters(self, file_filters):
        file_filters = util.return_list(file_filters)
        self.file_filters = file_filters

    def remove_file_filters(self, file_filters):
        file_filters = util.return_list(file_filters)
        for file_filter in file_filters:
            self.file_filters.remove(file_filter)

    def get_file_filters(self, filter_function=None):
        if filter_function is None:
            return self.file_filters
        else:
            return filter_function(self.file_filters)

    def add_blacklisted_filepaths(self, filepaths):
        filepaths = set(util.return_list(filepaths))
        self.blacklisted_filepaths.update(filepaths)

    def set_blacklisted_filepaths(self, filepaths):
        filepaths = set(util.return_list(filepaths))
        self.blacklisted_filepaths = filepaths

    def remove_blacklisted_filepaths(self, filepaths):
        filepaths = util.return_list(filepaths)
        for filepath in filepaths:
            self.blacklisted_filepaths.remove(filepath)

    def get_blacklisted_filepaths(self):
        return self.blacklisted_filepaths

    def add_file_filters(self, file_filters):
        file_filters = util.return_list(file_filters)
        self.file_filters.extend(file_filters)

    def collect_filepaths(self, directories):
        """
        Walk through the plugins' places and look for plugins.

        Return the candidates and number of plugins found.
        """
        plugin_files = set()
        directories = util.return_list(directories)
        for directory in directories:
            filepaths = util.get_filepaths_from_dir(directory)
            filepaths = self._filter_filepaths(filepaths)
            plugin_files.update(set(filepaths))

        plugin_files = self._remove_blacklisted(plugin_files)

        return plugin_files

    def _remove_blacklisted(self, filepaths):
        filepaths = util.return_list(filepaths)
        for filepath in filepaths:
            if filepath in self.blacklisted_filepaths:
                filepaths.remove(filepath)
        return filepaths

    def get_plugin_filepaths(self):
        return self.plugin_files

    def _filter_filepaths(self, filepaths):
        """
        helps iterate through all the file parsers
        """
        if self.file_filters:
            plugin_files = set()
            for file_filter in self.file_filters:
                plugin_paths = file_filter(filepaths)
                plugin_files.update(plugin_paths)
            filepaths = plugin_files

        return filepaths
