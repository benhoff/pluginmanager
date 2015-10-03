class IPlugin(object):
    """
    Simple interface to be inherited when creating a plugin.
    """
    def __init__(self):
        self.active = False
        self.config = None
        try:
            if not getattr(self, 'name'):
                self.name = self.__class__.__name__
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
        return None

    def check_configuration(self, configuration):
        # TODO: Implement a sensible default
        pass

    def configure(self, configuration):
        self.config = configuration
