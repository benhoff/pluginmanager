from pluginmanager import util


class FileManager(object):
    """
    `FileManager` manages the file filter state and is responible for
    collecting filepaths from a set of directories and filtering the files
    through the filters. Without file filters, this class acts as a
    passthrough, collecting and returning every file in a given directory.

    `FileManager` can also optionally manage the plugin filepath state through
    the use of the add/get/set plugin filepaths methods. Note that plugin
    interface is not automatically set up this way, although it is
    relatively trivial to do.
    """
    def __init__(self,
                 file_filters=None,
                 plugin_filepaths=None,
                 blacklisted_filepaths=None):

        """
        `FileFilters` are callable filters. Each filter must take in a
        set of filepaths and return back a set of filepaths. Each filter
        is applied independently to the set of filepaths and added to the
        return set.
        `FileFilters` can be a single object or an iterable

        `plugin_filepaths` are known plugin filepaths that can be stored
        in `FileManager`. Note that filepaths stored in the plugin filepaths
        are NOT automatically added when calling the `collect_filepaths`
        method. Recommend using absolute paths. `plugin_filepaths` can be a
        single object or an interable.

        `blacklisted_filepaths` are plugin filepaths that are not to be
        included in the collected filepaths. Recommend using absolute paths.
        `blacklisted_filepaths` can be a single object or an iterable.
        """

        if file_filters is None:
            file_filters = []
        if plugin_filepaths is None:
            plugin_filepaths = set()
        if blacklisted_filepaths is None:
            blacklisted_filepaths = set()

        self.file_filters = util.return_list(file_filters)
        # pep8
        to_abs_paths = util.to_absolute_paths

        self.plugin_filepaths = to_abs_paths(plugin_filepaths)
        self.blacklisted_filepaths = to_abs_paths(blacklisted_filepaths)

    def collect_filepaths(self, directories):
        """
        Collects and returns every filepath from each directory in
        `directories` that is filtered through the `file_filters`.
        If no `file_filters` are present, passes every file in directory
        as a result.
        Always returns a `set` object

        `directories` can be a object or an iterable. Recommend using
        absolute paths.
        """
        plugin_filepaths = set()
        directories = util.to_absolute_paths(directories)
        for directory in directories:
            filepaths = util.get_filepaths_from_dir(directory)
            filepaths = self._filter_filepaths(filepaths)
            plugin_filepaths.update(set(filepaths))

        plugin_filepaths = self._remove_blacklisted(plugin_filepaths)

        return plugin_filepaths

    def add_plugin_filepaths(self, filepaths, except_blacklisted=True):
        """
        Adds `filepaths` to the `self.plugin_filepaths`. Recommend passing
        in absolute filepaths. Method will attempt to convert to
        absolute paths if they are not already.

        `filepaths` can be a single object or an iterable

        If `except_blacklisted` is `True`, all `filepaths` that
        have been blacklisted will not be added.
        """
        filepaths = util.to_absolute_paths(filepaths)
        if except_blacklisted:
            filepaths = util.remove_from_set(filepaths,
                                             self.blacklisted_filepaths)

        self.plugin_filepaths.update(filepaths)

    def set_plugin_filepaths(self, filepaths, except_blacklisted=True):
        """
        Sets `filepaths` to the `self.plugin_filepaths`. Recommend passing
        in absolute filepaths. Method will attempt to convert to
        absolute paths if they are not already.

        `filepaths` can be a single object or an iterable.

        If `except_blacklisted` is `True`, all `filepaths` that
        have been blacklisted will not be set.
        """
        filepaths = util.to_absolute_paths(filepaths)
        if except_blacklisted:
            filepaths = util.remove_from_set(filepaths,
                                             self.blacklisted_filepaths)

        self.plugin_filepaths = filepaths

    def remove_plugin_filepaths(self, filepaths):
        """
        Removes `filepaths` from `self.plugin_filepaths`.
        Recommend passing in absolute filepaths. Method will
        attempt to convert to absolute paths if not passed in.

        `filepaths` can be a single object or an iterable.
        """
        filepaths = util.to_absolute_paths(filepaths)
        self.plugin_filepaths = util.remove_from_set(self.plugin_filepaths,
                                                     filepaths)

    def get_plugin_filepaths(self):
        """
        returns the plugin filepaths tracked internally as a `set` object.
        """
        return self.plugin_filepaths

    def set_file_filters(self, file_filters):
        """
        Sets internal file filters to `file_filters` by tossing old state.
        `file_filters` can be single object or iterable.
        """
        file_filters = util.return_list(file_filters)
        self.file_filters = file_filters

    def add_file_filters(self, file_filters):
        """
        Adds `file_filters` to the internal file filters.
        `file_filters` can be single object or iterable.
        """
        file_filters = util.return_list(file_filters)
        self.file_filters.extend(file_filters)

    def remove_file_filters(self, file_filters):
        """
        Removes the `file_filters` from the internal state.
        `file_filters` can be a single object or an iterable.
        """
        self.file_filters = util.remove_from_list(self.file_filters,
                                                  file_filters)

    def get_file_filters(self, filter_function=None):
        """
        Gets the file filters.
        `filter_function`, can be a user defined filter. Should be callable
        and return a list.
        """
        if filter_function is None:
            return self.file_filters
        else:
            return filter_function(self.file_filters)

    def add_blacklisted_filepaths(self, filepaths, remove_from_stored=True):
        """
        Add `filepaths` to blacklisted filepaths.
        If `remove_from_stored` is `True`, any `filepaths` in
        `plugin_filepaths` will be automatically removed.

        Recommend passing in absolute filepaths but method will attempt
        to convert to absolute filepaths based on current working directory.
        """
        filepaths = util.to_absolute_paths(filepaths)
        self.blacklisted_filepaths.update(filepaths)
        if remove_from_stored:
            self.plugin_filepaths = util.remove_from_set(self.plugin_filepaths,
                                                         filepaths)

    def set_blacklisted_filepaths(self, filepaths, remove_from_stored=True):
        """
        Sets internal blacklisted filepaths to filepaths.
        If `remove_from_stored` is `True`, any `filepaths` in
        `self.plugin_filepaths` will be automatically removed.

        Recommend passing in absolute filepaths but method will attempt
        to convert to absolute filepaths based on current working directory.
        """
        filepaths = util.to_absolute_paths(filepaths)
        self.blacklisted_filepaths = filepaths
        if remove_from_stored:
            self.plugin_filepaths = util.remove_from_set(self.plugin_filepaths,
                                                         filepaths)

    def remove_blacklisted_filepaths(self, filepaths):
        """
        Removes `filepaths` from blacklisted filepaths

        Recommend passing in absolute filepaths but method will attempt
        to convert to absolute filepaths based on current working directory.
        """
        filepaths = util.to_absolute_paths(filepaths)
        black_paths = self.blacklisted_filepaths
        black_paths = util.remove_from_set(black_paths, filepaths)

    def get_blacklisted_filepaths(self):
        """
        Returns the blacklisted filepaths as a set object.
        """
        return self.blacklisted_filepaths

    def _remove_blacklisted(self, filepaths):
        """
        internal helper method to remove the blacklisted filepaths
        from `filepaths`.
        """
        filepaths = util.remove_from_set(filepaths, self.blacklisted_filepaths)
        return filepaths

    def _filter_filepaths(self, filepaths):
        """
        helps iterate through all the file parsers
        each filter is applied individually to the
        same set of `filepaths`
        """
        if self.file_filters:
            plugin_filepaths = set()
            for file_filter in self.file_filters:
                plugin_paths = file_filter(filepaths)
                plugin_filepaths.update(plugin_paths)
        else:
            plugin_filepaths = filepaths

        return plugin_filepaths
