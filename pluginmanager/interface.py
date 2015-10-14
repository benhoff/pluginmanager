import inspect
from .file_locator import FileLocator
from .plugin_manager import PluginManager
from .module_loader import ModuleLoader
from .directory_manager import DirectoryManager
from .instance_manager import InstanceManager


class Interface(object):
    def __init__(self,
                 file_locator=FileLocator(),
                 module_loader=ModuleLoader(),
                 plugin_manager=PluginManager(),
                 instance_manager=InstanceManager(),
                 auto_manage_state=True):

        self.managing_state = auto_manage_state
        self.directory_manager = DirectoryManager()
        self.file_locator = file_locator
        self.module_loader = module_loader
        self.plugin_manager = plugin_manager
        self.instance_manager = instance_manager

    def track_site_package_paths(self):
        return self.directory_manager.add_site_packages_paths()

    def collect_plugin_directories(self, directories=None):
        if directories is None:
            directories = self.directory_manager.get_plugin_directories()
        return self.directory_manager.collect_plugin_directories(directories)

    def collect_plugin_filepaths(self, directories=None):
        if directories is None:
            directories = self.get_plugin_directories()
        return self.file_locator.collect_filepaths(directories)

    def collect_modules(self, filepaths=None):
        if filepaths is None:
            filepaths = self.collect_plugin_filepaths()

        return self.module_loader.collect_modules(filepaths)

    def collect_plugins(self, modules=None):
        if modules is None:
            modules = self.collect_modules()
        plugins = self.module_loader.get_plugins_from_modules(modules)
        if self.managing_state:
            self.add_plugins(plugins)
            self.instantiate_plugins(plugins)
        return plugins

    def reload_modules(self, module_or_module_name):
        self.module_loader.reload_module(module_or_module_name)

    def set_plugins(self, plugins):
        self.plugin_manager.set_plugins(plugins)

    def add_plugins(self, plugins):
        self.plugin_manager.add_plugins(plugins)

    def remove_plugins(self, plugins):
        self.plugin_manager.remove_plugins(plugins)

    def get_plugins(self):
        return self.plugin_manager.get_plugins()

    def blacklist_plugin(self, plugins):
        self.plugin_manager.blacklist_plugins(plugins)

    def add_instances(self, instances):
        self.instance_manager.add_instances(instances)

    def set_instances(self, instances):
        self.instance_manager.set_instances(instances)

    def instantiate_plugins(self, classes=None):
        if self.managing_state:
            isclass = inspect.isclass
            plugin_classes = [x for x in self.get_plugins() if isclass(x)]
            self.instance_manager.add_instances(plugin_classes)

    def get_instances(self):
        return self.instance_manager.instances

    def activate_instances(self):
        self.instance_manager.activate_instances()

    def deactivate_instances(self):
        self.instance_manager.deactivate_instances()

    def configure_instances(self, config):
        self.instance_manager.configure_instances(config)

    def get_configuration_templates(self):
        return self.instance_manager.get_configuration_templates()

    def check_configurations(self):
        pass
    
    def add_plugin_directories(self, paths):
        self.directory_manager.add_directories(paths)

    def get_plugin_directories(self):
        return self.directory_manager.get_directories()

    def remove_plugin_directories(self, paths):
        self.directory_manager.remove_directories(paths)

    def set_plugin_directories(self, paths):
        self.directory_manager.set_directories(paths)

    def add_plugin_filepaths(self, filepaths):
        self.file_locator.add_plugin_filepaths(filepaths)

    def get_plugin_filepaths(self):
        return self.file_locator.get_plugin_filepaths()

    def remove_plugin_filepaths(self, filepaths):
        self.file_locator.remove_plugin_filepaths(filepaths)

    def set_plugin_filepaths(self, filepaths):
        self.file_locator.set_plugin_filepaths(filepaths)

    def add_blacklisted_filepaths(self, filepaths):
        self.module_loader.add_blacklisted_filepaths(filepaths)

    def get_blacklisted_filepaths(self):
        return self.module_loader.blacklisted_filepaths

    def set_blacklisted_filepaths(self, filepaths):
        self.module_loader.set_blacklisted_filepaths(filepaths)

    def remove_blacklisted_filepaths(self, filepaths):
        self.module_loader.remove_blacklisted_filepaths(filepaths)

    def add_to_loaded_modules(self, modules):
        self.module_loader.add_to_loaded_modules(modules)

    def get_loaded_modules(self):
        return self.module_loader.get_loaded_modules()

    def add_file_getters(self, file_getters):
        self.file_locator.add_file_getters(file_getters)

    def get_file_getters(self):
        return self.file_locator.file_getters

    def remove_file_getters(self, file_getters):
        self.file_locator.remove_file_getters(file_getters)

    def set_file_getters(self, file_getters):
        self.file_locator.set_file_getters(file_getters)
