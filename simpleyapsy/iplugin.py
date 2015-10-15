class IPlugin(object):
    """
    Simple interface to be inherited when creating a plugin.
    """
    CONFIG_TEMPLATE = {}

    def __init__(self):
        self.active = False
        self.config = None
        try:
            getattr(self, 'name')
        except AttributeError:
            self.name = self.__class__.__name__

    def activate(self):
        """
        Called at plugin activation.
        """
        self.active = True

    def deactivate(self):
        """
        Called when the plugin is disabled.
        """
        self.active = False

    def get_configuration_template(self):
        """
        If your plugin needs a configuration, override this method and return
        a configuration template.
        For example a dictionary like:
        return {'LOGIN' : 'example@example.com', 'PASSWORD' : 'password'}
        Note: if this method returns None, the plugin won't be configured
        """
        return self.CONFIG_TEMPLATE

    def check_configuration(self, configuration):
        config_template = self.get_configuration_template()
        for key in config_template.keys():
            if key not in configuration:
                error = '{} doesn\'t contain the key {}'.format(configuration,
                                                                key)

                raise Exception(error)
        return True

    def configure(self, configuration):
        self.config = configuration
