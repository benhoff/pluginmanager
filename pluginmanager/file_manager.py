from pluginmanager import util


class FileManager(object):
    """
    `FileManager` manages the file filter state and is responible for applying
    the file filters to the filepaths gotten from the
    """
    def __init__(self,
                 file_filters=None):

        if file_filters is None:
            file_filters = []

        file_filters = util.return_list(file_filters)
        self.file_filters = file_filters
        self.plugin_files = set()
        self.blacklisted_filepaths = set()

    def add_plugin_filepaths(self, filepaths):
        self.plugin_files.update(util.return_set(filepaths))

    def set_plugin_filepaths(self, filepaths):
        self.plugin_files = util.return_set(filepaths)

    def remove_plugin_filepaths(self, filepaths):
        util.remove_from_set(self.plugin_files, filepaths)

    def set_file_filters(self, file_filters):
        file_filters = util.return_list(file_filters)
        self.file_filters = file_filters

    def remove_file_filters(self, file_filters):
        util.remove_from_list(self.file_filters, file_filters)

    def get_file_filters(self, filter_function=None):
        if filter_function is None:
            return self.file_filters
        else:
            return filter_function(self.file_filters)

    def add_blacklisted_filepaths(self, filepaths):
        filepaths = util.return_set(filepaths)
        self.blacklisted_filepaths.update(filepaths)

    def set_blacklisted_filepaths(self, filepaths):
        filepaths = util.return_set(filepaths)
        self.blacklisted_filepaths = filepaths

    def remove_blacklisted_filepaths(self, filepaths):
        util.remove_from_set(self.blacklisted_filepaths, filepaths)

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
        util.remove_from_set(filepaths, self.blacklisted_filepaths)
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
