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

    def _handle_class_instance(self, klass):
        if not self.instantiate_classes:
            return
        if self.unique_instances and self._unique_class(klass):
            self.plugins.append(klass())
        elif not self.unique_instances:
            self.plugins.append(klass())

    def _handle_object_instance(self, instance):
        if self.unique_instances:
            klass = type(instance)
            instance_unique = self._unique_class(klass)
            if instance_unique:
                self.plugins.append(instance)
        else:
            self.plugins.append(instance)

    def _instance_parser(self, plugins):
        plugins = util.return_list(plugins)
        for instance in plugins:
            if inspect.isclass(instance):
                self._handle_class_instance(instance)
            else:
                self._handle_object_instance(instance)

    def activate_plugins(self):
        for instance in self.plugins:
            instance.activate()

    def deactivate_plugins(self):
        for instance in self.plugins:
            instance.deactivate()

    def get_configuration_templates(self):
        config = {}
        for instance in self.plugins:
            # TODO: think about name clashing?
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

    def get_plugins(self):
        return self.plugins

    def blacklist_plugins(self, plugins):
        self.blacklisted_plugins.extend(plugins)

    def add_plugins(self, plugins):
        plugins = util.return_list(plugins)
        for plugin in plugins:
            if plugin not in self.blacklisted_plugins:
                self.plugins.append(plugin)

    def set_plugins(self, plugins):
        plugins = util.return_list(plugins)
        self.plugins = []

        for plugin in plugins:
            if plugin not in self.blacklisted_plugins:
                self.plugins.append(plugin)
