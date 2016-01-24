import inspect
from . import util
from .iplugin import IPlugin


class PluginManager(object):
    """
    PluginManager manages the plugin state. It can automatically
    instantiate classes and enforce uniqueness, which it does by default.
    """
    def __init__(self,
                 unique_instances=True,
                 instantiate_classes=True,
                 plugins=None,
                 blacklisted_plugins=None):
        """
        `unique_instances` determines if all plugins have to be unique.
        This will also ensure that no two instances of the same class are
        tracked internally.

        `instantiate_classes` tracks to see if the class should automatically
        instantiate class objects that are passed in.
        `plugins` can be a single obj or iterable
        `blacklisted plugins` can be a single obj or iterable
        """
        self.unique_instances = unique_instances
        self.instantiate_classes = instantiate_classes

        if plugins is None:
            plugins = []
        if blacklisted_plugins is None:
            blacklisted_plugins = []

        self.plugins = util.return_list(plugins)
        self.blacklisted_plugins = util.return_list(blacklisted_plugins)

    def get_plugins(self, filter_function=None):
        """
        Gets out the plugins from the internal state. Returns a list object.
        If the optional filter_function is supplied, applies the filter
        function to the arguments before returning them. Filters should
        be callable and take a list argument of plugins.
        """
        plugins = self.plugins
        if filter_function is not None:
            plugins = filter_function(plugins)
        return plugins

    def add_plugins(self, plugins):
        """
        Adds plugins to the internal state. `plugins` may be a single object
        or an iterable.

        If `instantiate_classes` is True and the plugins
        have class instances in them, attempts to instatiate the classes.

        If `unique_instances` is True and duplicate instances are passed in,
        this method will not track the new instances internally.
        """
        self._instance_parser(plugins)

    def set_plugins(self, plugins):
        """
        sets plugins to the internal state. `plugins` may be a single object
        or an iterable.

        If `instatntiate_classes` is True and the plugins
        have class instances in them, attempts to instatiate the classes.

        If `unique_instances` is True and duplicate instances are passed in,
        this method will not track the new instances internally.
        """
        self.plugins = []
        self._instance_parser(plugins)

    def remove_plugins(self, plugins):
        """
        removes `plugins` from the internal state

        `plugins` may be a single object or an iterable.
        """
        util.remove_from_list(self.plugins, plugins)

    def remove_instance(self, instances):
        """
        removes `instances` from the internal state.

        Note that this method is syntatic sugar for the
        `remove_plugins` acts as a passthrough for that
        function.
        `instances` may be a single object or an iterable
        """
        self.remove_plugins(instances)

    def _get_instance(self, klasses):
        """
        internal method that gets every instance of the klasses
        out of the internal plugin state.
        """
        return [x for x in self.plugins if isinstance(x, klasses)]

    def get_instances(self, filter_function=IPlugin):
        """
        Gets instances out of the internal state using
        the default filter supplied in filter_function.
        By default, it is the class IPlugin.

        Can optionally pass in a list or tuple of classes
        in for `filter_function` which will accomplish
        the same goal.

        lastly, a callable can be passed in, however
        it is up to the user to determine if the
        objects are instances or not.
        """
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
        IPlugin.
        `classes` may be a single object or an iterable.
        """
        classes = util.return_list(classes)
        for klass in classes:
            IPlugin.register(klass)

    def _instance_parser(self, plugins):
        """
        internal method to parse instances of plugins.

        Determines if each class is a class instance or
        object instance and calls the appropiate handler
        method.
        """
        plugins = util.return_list(plugins)
        for instance in plugins:
            if inspect.isclass(instance):
                self._handle_class_instance(instance)
            else:
                self._handle_object_instance(instance)

    def _handle_class_instance(self, klass):
        """
        handles class instances. If a class is blacklisted, returns.
        If uniuqe_instances is True and the class is unique, instantiates
        the class and adds the new object to plugins.

        If not unique_instances, creates and adds new instance to plugin
        state
        """
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
        """
        helper method that attempts to activate plugins
        checks to see if plugin has method call before
        calling it.
        """
        for instance in self.get_instances():
            if hasattr(instance, 'activate'):
                instance.activate()

    def deactivate_plugins(self):
        """
        helper method that attempts to deactivate plugins.
        checks to see if plugin has method call before
        calling it.
        """
        for instance in self.get_instances():
            if hasattr(instance, 'deactivate'):
                instance.deactivate()

    def _unique_class(self, cls):
        """
        internal method to check if any of the plugins are instances
        of a given cls
        """
        return not any(isinstance(obj, cls) for obj in self.plugins)

    def add_blacklisted_plugins(self, plugins):
        """
        add blacklisted plugins.
        `plugins` may be a single object or iterable.
        """
        plugins = util.return_list(plugins)
        self.blacklisted_plugins.extend(plugins)

    def set_blacklisted_plugins(self, plugins):
        """
        sets blacklisted plugins.
        `plugins` may be a single object or iterable.
        """
        plugins = util.return_list(plugins)
        self.blacklisted_plugins = plugins

    def get_blacklisted_plugins(self):
        """
        gets blacklisted plugins tracked in the internal state
        Returns a list object.
        """
        return self.blacklisted_plugins

    def remove_blacklisted_plugins(self, plugins):
        """
        removes `plugins` from the blacklisted plugins.
        `plugins` may be a single object or iterable.
        """
        util.remove_from_list(self.blacklisted_plugins, plugins)
