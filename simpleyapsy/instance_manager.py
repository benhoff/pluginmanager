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

    def configure_instances(self, config):
        pass

    def activate_instances(self):
        pass

    def deactivate_instances(self):
        pass

    def get_configuration_template(self):
        pass

    def check_configuration(self):
        pass
