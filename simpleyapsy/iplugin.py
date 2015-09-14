class IPlugin(object):
    """
    The most simple interface to be inherited when creating a plugin.
    """

    def __init__(self):
        self.is_activated = False

    def activate(self):
        """
        Called at plugin activation.
        """
        self.is_activated = True

    def deactivate(self):
        """
        Called when the plugin is disabled.
        """
        self.is_activated = False

