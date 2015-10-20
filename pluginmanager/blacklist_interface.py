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
        pass

    def get_blacklisted_directories(self):
        pass

    def set_blacklisted_directories(self, directories):
        pass

    def remove_blacklisted_directories(self, directories):
        pass

    def add_blacklisted_filepaths(self, filepaths):
        self.module_manager.add_blacklisted_filepaths(filepaths)

    def get_blacklisted_filepaths(self):
        return self.module_manager.blacklisted_filepaths

    def set_blacklisted_filepaths(self, filepaths):
        self.module_manager.set_blacklisted_filepaths(filepaths)

    def remove_blacklisted_filepaths(self, filepaths):
        self.module_manager.remove_blacklisted_filepaths(filepaths)

    def add_blacklisted_plugins(self, plugins):
        pass

    def get_blacklisted_plugins(self):
        pass

    def set_blacklisted_plugins(self, plugins):
        pass

    def remove_blacklisted_plugins(self, plugins):
        pass
