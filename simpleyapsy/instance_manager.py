from simpleyapsy import util


class InstanceManager(object):
    def __init__(self):
        self.instances = []

    def add_instances(self, instances):
        instances = util.return_list(instances)
        self.instances.extend(instances)

    def set_instances(self, instances):
        instances = util.return_list(instances)
        self.instances = instances

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
