class IPlugin(object):
    """
    Simple interface to be inherited when creating a plugin.
    """

    def __init__(self):
        self.active = False

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

