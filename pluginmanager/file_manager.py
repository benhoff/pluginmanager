from pluginmanager import util


class FileManager(object):
    """
    `FileManager` manages the file filter state and is responible for
    collecting filepaths from a set of directories and filtering the files
    through the filters. Without file filters, this class acts as a
    passthrough, collecting and returning every file in a given directory.

    `FileManager` can also optionally manage the plugin filepath state through
    the use of the add/get/set plugin filepaths. Note that plugin interface is
    not automatically set up this way, although it remains relatively trivial.
    """
    def __init__(self,
                 file_filters=None,
                 plugin_files=None,
                 blacklisted_filepaths=None):

        """
        `FileFilters` are callable filters. Each filter must take in a
        set of filepaths and return back a set of filepaths. Each filter
        is applied independently to the filepaths and added to the
        return set (and as a function of using a `set` object, without
        any repeats).
        `FileFilters` can be a single object or an iterable

        `plugin_files` are known plugin filepaths that can be stored
        in `FileManager`. Note that filepaths stored in the plugin filepaths
        are NOT automatically added when calling the `collect_filepaths`
        method and additional work is required on the interface level
        to achieve a level of automation.

        `blacklisted_filepaths` are plugin filepaths that are not to be
        included in the collected filepaths.
        """

        if file_filters is None:
            file_filters = []
        if plugin_files is None:
            plugin_files = set()
        if blacklisted_filepaths is None:
            blacklisted_filepaths = set()

        self.file_filters = util.return_list(file_filters)
        self.plugin_files = util.return_set(plugin_files)
        self.blacklisted_filepaths = util.return_set(blacklisted_filepaths)

    def collect_filepaths(self, directories):
        """
        Collects and returns every filepath from each directory in
        `directories` that is filetered through the internal `file_filters`

        directories can be a object or an iterable

        Returns a `set` object of plugin filepaths
        """
        plugin_files = set()
        directories = util.return_list(directories)
        for directory in directories:
            filepaths = util.get_filepaths_from_dir(directory)
            filepaths = self._filter_filepaths(filepaths)
            plugin_files.update(set(filepaths))

        plugin_files = self._remove_blacklisted(plugin_files)

        return plugin_files

    def add_plugin_filepaths(self, filepaths, except_blacklisted=True):
        """
        Adds `filepaths` to the `self.plugin_files`. Recommend passing
        in absolute filepaths. Method will attempt to convert to
        absolute paths if they are not already.

        `filepaths` can be a single object or an iterable

        If `except_blacklisted` is `True`, all `filepaths` that
        have been blacklisted will be removed.
        """
        filepaths = util.to_absolute_paths(filepaths)
        if except_blacklisted:
            filepaths = util.remove_from_set(filepaths,
                                             self.blacklisted_filepaths)

        self.plugin_files.update(filepaths)

    def set_plugin_filepaths(self, filepaths, except_blacklisted=True):
        """
        Sets `filepaths` to the `self.plugin_files`. Recommend passing
        in absolute filepaths. Method will attempt to convert to
        absolute paths if they are not already.

        `filepaths` can be a single object or an iterable.

        If `except_blacklisted` is `True`, all `filepaths` that
        have been blacklisted will be removed.
        """
        filepaths = util.to_absolute_paths(filepaths)
        if except_blacklisted:
            filepaths = util.remove_from_set(filepaths,
                                             self.blacklisted_filepaths)

        self.plugin_files = filepaths

    def remove_plugin_filepaths(self, filepaths):
        """
        Removes `filepaths` from `self.plugin_filepaths`.
        Recommend passing in absolute filepaths. Method will
        attempt to convert to absolute paths if not passed in.

        `filepaths` can be a single object or an iterable.
        """
        filepaths = util.to_absolute_paths(filepaths)
        util.remove_from_set(self.plugin_files, filepaths)

    def get_plugin_filepaths(self):
        """
        returns the plugin files tracked internally
        """
        return self.plugin_files

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

    def add_blacklisted_filepaths(self, filepaths, remove_from_stored=True):
        filepaths = util.return_set(filepaths)
        self.blacklisted_filepaths.update(filepaths)
        if remove_from_stored:
            util.remove_from_set(self.plugin_files, filepaths)

    def set_blacklisted_filepaths(self, filepaths, remove_from_stored=True):
        filepaths = util.return_set(filepaths)
        self.blacklisted_filepaths = filepaths
        if remove_from_stored:
            util.remove_from_set(self.plugin_files, filepaths)

    def remove_blacklisted_filepaths(self, filepaths):
        util.remove_from_set(self.blacklisted_filepaths, filepaths)

    def get_blacklisted_filepaths(self):
        return self.blacklisted_filepaths

    def add_file_filters(self, file_filters):
        file_filters = util.return_list(file_filters)
        self.file_filters.extend(file_filters)

    def _remove_blacklisted(self, filepaths):
        util.remove_from_set(filepaths, self.blacklisted_filepaths)
        return filepaths

    def _filter_filepaths(self, filepaths):
        """
        helps iterate through all the file parsers
        each filter is applied individually to the
        same set of `filepaths`
        """
        if self.file_filters:
            plugin_files = set()
            for file_filter in self.file_filters:
                plugin_paths = file_filter(filepaths)
                plugin_files.update(plugin_paths)
            filepaths = plugin_files

        return filepaths
