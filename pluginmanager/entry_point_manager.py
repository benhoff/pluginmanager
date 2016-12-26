import pkg_resources
from pluginmanager import util


class EntryPointManager(object):
    """
    Entry points are an advanced python packaging systems whereby installing
    using pip automagically makes the package available to the program.
    This class manages the state associated with the entry points and is
    responsible for collecting plugins using entry points.
    """
    def __init__(self, entry_point_names=None):
        if entry_point_names is None:
            entry_point_names = set()

        self.entry_point_names = util.return_set(entry_point_names)

    def add_entry_points(self, names):
        """
        adds `names` to the internal collection of entry points to track

        `names` can be a single object or an iterable but
        must be a string or iterable of strings.
        """
        names = util.return_set(names)
        self.entry_point_names.update(names)

    def set_entry_points(self, names):
        """
        sets the internal collection of entry points to be
        equal to `names`

        `names` can be a single object or an iterable but
        must be a string or iterable of strings.
        """
        names = util.return_set(names)
        self.entry_point_names = names

    def remove_entry_points(self, names):
        """
        removes `names` from the set of entry points to track.

        `names` can be a single object or an iterable.
        """
        names = util.return_set(names)
        util.remove_from_set(self.entry_point_names,
                             names)

    def get_entry_points(self):
        """
        returns a set of all the entry points tracked internally
        """
        return self.entry_point_names

    def collect_plugins(self,
                        entry_points=None,
                        verify_requirements=False,
                        return_dict=False):

        """
        collects the plugins from the `entry_points`. If `entry_points` is not
        explicitly defined, this method will pull from the internal state
        defined using the add/set entry points methods.

        `entry_points` can be a single object or an iterable, but must be
        either a string or an iterable of strings.

        returns a list of plugins or an empty list.
        """

        if entry_points is None:
            entry_points = self.entry_point_names
        else:
            entry_points = util.return_set(entry_points)

        plugins = []
        plugin_names = []
        for name in entry_points:
            for entry_point in pkg_resources.iter_entry_points(name):
                if (hasattr(entry_point, 'resolve') and
                        hasattr(entry_point, 'require')):

                    if verify_requirements:
                        entry_point.require()

                    plugin = entry_point.resolve()
                else:
                    plugin = entry_point.load()

                plugins.append(plugin)
                plugin_names.append(entry_point.name)

        if return_dict:
            return {n: v for n, v in zip(plugin_names, plugins)}

        return plugins, plugin_names
