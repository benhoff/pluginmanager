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
        pass

    def configure_instances(self, config):
        pass

    def check_configurations(self):
        pass
