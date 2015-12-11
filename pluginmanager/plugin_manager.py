import inspect
from . import util
from .iplugin import IPlugin


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

    def remove_plugins(self, plugins):
        util.remove_from_list(self.plugins, plugins)

    def remove_instance(self, instances):
        self.remove_plugins(instances)

    def _get_instance(self, klasses):
        return [x for x in self.plugins if isinstance(x, klasses)]

    def get_instances(self, filter_function=IPlugin):
        if isinstance(filter_function, (list, tuple)):
            return self._get_instance(filter_function)
        elif inspect.isclass(filter_function):
            return self._get_instance(filter_function)
        elif filter_function is None:
            return self.plugins
        else:
            return filter_function(self.plugins)

    def register_classes(self, classes):
        """
        Register classes as plugins that are not subclassed from
        IPlugin
        """
        classes = util.return_list(classes)
        for klass in classes:
            IPlugin.register(klass)

    def _instance_parser(self, plugins):
        plugins = util.return_list(plugins)
        for instance in plugins:
            if inspect.isclass(instance):
                self._handle_class_instance(instance)
            else:
                self._handle_object_instance(instance)

    def _handle_class_instance(self, klass):
        if (klass in self.blacklisted_plugins or not
                self.instantiate_classes or
                klass == IPlugin):
            return
        elif self.unique_instances and self._unique_class(klass):
            self.plugins.append(klass())
        elif not self.unique_instances:
            self.plugins.append(klass())

    def _handle_object_instance(self, instance):
        klass = type(instance)

        if klass in self.blacklisted_plugins:
            return
        elif self.unique_instances:
            if self._unique_class(klass):
                self.plugins.append(instance)
            else:
                return
        else:
            self.plugins.append(instance)

    def activate_plugins(self):
        for instance in self.get_instances():
            instance.activate()

    def deactivate_plugins(self):
        for instance in self.get_instances():
            instance.deactivate()

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
        util.remove_from_list(self.blacklisted_plugins, plugins)
