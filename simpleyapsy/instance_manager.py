import inspect
from simpleyapsy import util


class InstanceManager(object):
    def __init__(self,
                 unique_instances=True,
                 instantiate_classes=True):

        self.unique_instances = unique_instances
        self.instantiate_classes = instantiate_classes
        self.instances = []

    def _handle_class_instance(self, klass):
        if not self.instantiate_classes:
            return
        if self.unique_instances and self._unique_class(klass):
            self.instances.append(klass())
        elif not self.unique_instances:
            self.instances.append(klass())

    def _handle_object_instance(self, instance):
        if self.unique_instances:
            klass = type(instance)
            instance_unique = self._unique_class(klass)
            if instance_unique:
                self.instances.append(instance)
        else:
            self.instances.append(instance)

    def _instance_parser(self, instances):
        instances = util.return_list(instances)
        for instance in instances:
            if inspect.isclass(instance):
                self._handle_class_instance(instance)
            else:
                self._handle_object_instance(instance)

    def add_instances(self, instances):
        self._instance_parser(instances)

    def set_instances(self, instances):
        self.instances = []
        self._instance_parser(instances)

    def get_instances(self):
        return self.instances

    def activate_instances(self):
        for instance in self.instances:
            instance.activate()

    def deactivate_instances(self):
        for instance in self.instances:
            instance.deactivate()

    def get_configuration_templates(self):
        config = {}
        for instance in self.instances:
            # TODO: think about name clashing?
            config[instance.name] = instance.get_configuration_template()
        return config

    def configure_instances(self, config):
        for instance in self.instances:
            instance.configure(config[instance.name])

    def check_configurations(self, config):
        results = []
        for instance in self.instances:
            name = instance.name
            config_instance = config[name]
            result = instance.check_configuration(config_instance)
            results.append((name, result, config_instance))
        return results

    def _parse_instance_helper(self, instances, unique_override=False):
        instances = util.return_list(instances)
        for instance in instances:
            if (self.unique_instances and
                    self._unique_instance(instance) and not
                    unique_override):

                pass

    def _unique_class(self, cls):
        return not any(isinstance(obj, cls) for obj in self.instances)
