import inspect
from pluginmanager import util


class PluginManager(object):
    def __init__(self,
                 unique_instances=True,
                 instantiate_classes=True):

        self.plugins = []
        self.unique_instances = unique_instances
        self.instantiate_classes = instantiate_classes
        self.blacklisted_plugins = []

    def get_plugins(self, filter_function=None):
        plugins = self.plugins
        if filter_function is not None:
            plugins = filter_function(plugins)
        return plugins

    def add_plugins(self, plugins):
        self._instance_parser(plugins)

    def set_plugins(self, plugins):
        self.plugins = []
        self._instance_parser(plugins)

    def _instance_parser(self, plugins):
        plugins = util.return_list(plugins)
        for instance in plugins:
            if inspect.isclass(instance):
                self._handle_class_instance(instance)
            else:
                self._handle_object_instance(instance)

    def _handle_class_instance(self, klass):
        if not self.instantiate_classes or klass in self.blacklisted_plugins:
            return
        if self.unique_instances and self._unique_class(klass):
            self.plugins.append(klass())
        elif not self.unique_instances:
            self.plugins.append(klass())

    def _handle_object_instance(self, instance):
        klass = type(instance)
        instance_is_unique = self._unique_class(klass)

        if klass in self.blacklisted_plugins:
            return
        elif self.unique_instances and instance_is_unique:
            self.plugins.append(instance)
        else:
            self.plugins.append(instance)

    def activate_plugins(self):
        for instance in self.plugins:
            instance.activate()

    def deactivate_plugins(self):
        for instance in self.plugins:
            instance.deactivate()

    def get_configuration_templates(self):
        config = {}
        names = [plugin.name for plugin in self.get_plugins(
        for instance in self.plugins:
            name = instance.name
            if name in config:
                old_config = config[name]
                extended_name = '{}.{}.{}'.format(instance.__module__, instance.__class__, name)
            else
            config[instance.name] = instance.get_configuration_template()
        return config

    def configure_plugins(self, config):
        for instance in self.plugins:
            instance.configure(config[instance.name])

    def check_configurations(self, config):
        results = []
        for instance in self.plugins:
            name = instance.name
            config_instance = config[name]
            result = instance.check_configuration(config_instance)
            results.append((name, result, config_instance))
        return results

    def _parse_instance_helper(self, plugins, unique_override=False):
        plugins = util.return_list(plugins)
        for instance in plugins:
            if (self.unique_instances and
                    self._unique_instance(instance) and not
                    unique_override):

                pass

    def _unique_class(self, cls):
        return not any(isinstance(obj, cls) for obj in self.plugins)

    def add_blacklisted_plugins(self, plugins):
        plugins = util.return_list(plugins)
        self.blacklisted_plugins.extend(plugins)

    def set_blacklisted_plugins(self, plugins):
        plugins = util.return_list(plugins)
        self.blacklisted_plugins = plugins

    def get_blacklisted_plugins(self):
        return self.blacklisted_plugins

    def remove_blacklisted_plugins(self, plugins):
        plugins = util.return_list(plugins)
        for plugin in plugins:
            self.blacklisted_plugins.remove(plugin)
