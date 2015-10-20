class FilterIterface(object):
    def __init__(self,
                 directory_manager,
                 file_manager,
                 module_manager,
                 plugin_manager):
        
        self.directory_manager = directory_manager
        self.file_manager = file_manager
        self.module_manager = module_manager
        self.plugin_manager = plugin_manager

    def add_file_filters(self, file_filters):
        self.file_manager.add_file_filters(file_filters)

    def get_file_filters(self):
        return self.file_manager.file_filters

    def remove_file_filters(self, file_filters):
        self.file_manager.remove_file_filters(file_filters)

    def set_file_filters(self, file_filters):
        self.file_manager.set_file_filters(file_filters)
        
    def add_module_filters(self, file_filters):
        pass

    def get_module_filters(self):
        pass

    def remove_module_filters(self, file_filters):
        pass

    def set_module_filters(self, file_filters):
        pass
