from pluginmanager import util


class FileManager(object):
    """
    `FileManager` manages the file filter state and is responible for collecting
    filepaths given a list of directories and applying the file filters to the
    collected filepaths
    """
    def __init__(self,
                 file_filters=None,
                 plugin_files=None,
                 blacklisted_filepaths=None):
        """
        `FileFilters` are callable filters. Each filter must take in a 
        set of filepaths and return back a set of filepaths. 
        `FileFilters` can be a single object or an iterable

        `plugin_files` are known plugin filepaths that can be stored
        in `FileManager`. Note that filepaths stored in the plugin filepaths
        are not automatically added when calling the `collect_
        """

        if file_filters is None:
            file_filters = []
        if plugin_files is None:
            plugin_files = set()
        if blacklisted_filepaths is None:
            blacklisted_filepaths = set()

        file_filters = util.return_list(file_filters)
        self.file_filters = file_filters
        self.plugin_files = plugin_files
        self.blacklisted_filepaths = blacklisted_filepaths

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
