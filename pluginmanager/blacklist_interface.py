class BlacklistInterface(object):
    def __init__(self,
                 directory_manager,
                 file_manager,
                 module_manager,
                 plugin_manager):

        self.directory_manager = directory_manager
        self.file_manager = file_manager
        self.module_manager = module_manager
        self.plugin_manager = plugin_manager

    def add_blacklisted_directories(self, directories):
        self.directory_manager.add_blacklisted_directories(directories)

    def get_blacklisted_directories(self):
        return self.directory_manager.get_blacklisted_directories()

    def set_blacklisted_directories(self, directories):
        self.directory_manager.set_blacklisted_directories(directories)

    def remove_blacklisted_directories(self, directories):
        self.directory_manager.remove_blacklisted_directories(directories)

    def add_blacklisted_filepaths(self, filepaths):
        self.file_manager.add_blacklisted_filepaths(filepaths)

    def get_blacklisted_filepaths(self):
        return self.file_manager.get_blacklisted_filepaths()

    def set_blacklisted_filepaths(self, filepaths):
        self.file_manager.set_blacklisted_filepaths(filepaths)

    def remove_blacklisted_filepaths(self, filepaths):
        self.file_manager.remove_blacklisted_filepaths(filepaths)

    def add_blacklisted_plugins(self, plugins):
        self.plugin_manager.add_blacklisted_plugins(plugins)

    def get_blacklisted_plugins(self):
        return self.plugin_manager.get_blacklisted_plugins()

    def set_blacklisted_plugins(self, plugins):
        self.plugin_manager.set_blacklisted_plugins(plugins)

    def remove_blacklisted_plugins(self, plugins):
        self.plugin_manager.remove_blacklisted_plugins(plugins)
