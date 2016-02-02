import pkg_resources
from pluginmanager import util


class EntryPointManager(object):
    def __init__(self, entry_point_names=None):
        if entry_point_names is None:
            entry_point_names = set()

        self.entry_point_names = util.return_set(entry_point_names)

    def add_entry_points(self, names):
        names = util.return_set(names)
        self.entry_point_names.update(names)

    def set_entry_points(self, names):
        names = util.return_set(names)
        self.entry_point_names = names

    def remove_entry_points(self, names):
        names = util.return_set(names)
        util.remove_from_set(self.entry_point_names,
                             names)

    def get_entry_points(self):
        return self.entry_point_names

    def collect_plugins(self,
                        entry_points=None,
                        verify_requirements=False):

        if entry_points is None:
            entry_points = self.entry_point_names
        else:
            entry_points = util.return_set(entry_points)

        plugins = []
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

        return plugins
