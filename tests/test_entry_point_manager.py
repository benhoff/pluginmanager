import unittest
import setuptools
from .compat import tempfile
from pluginmanager.entry_point_manager import EntryPointManager


class TestEntryPointManager(unittest.TestCase):
    def setUp(self):
        self.manager = EntryPointManager()

    def test_add_entry_point(self):
        """
        add a string using the prescribed method and then
        make sure it is in the correct data member
        """
        test = 'test'
        self.manager.add_entry_points(test)
        self.assertIn(test, self.manager.entry_point_names)

    def test_set_entry_points(self):
        """
        add some previous state and then use the prescribed
        method to set the state. Check to make sure the previous state
        is not there and that the new state is.
        """
        previous_state = 'previous'
        self.manager.add_entry_points(previous_state)
        new_state = 'test'
        self.manager.set_entry_points(new_state)
        entry_points = self.manager.get_entry_points()

        self.assertNotIn(previous_state, entry_points)
        self.assertIn(new_state, entry_points)

    def test_remove_entry_points(self):
        """
        add a string to the entry points and then remove it using the
        prescribed method. Make sure that the string is not still there.
        """
        removed = 'test'
        self.manager.add_entry_points(removed)
        self.assertIn(removed, self.manager.entry_point_names)
        self.manager.remove_entry_points(removed)
        self.assertNotIn(removed, self.manager.entry_point_names)

    def test_collect_plugins(self):
        entry_points = 'distutils.commands'
        plugins = self.manager.collect_plugins(entry_points)
        self.assertIn(setuptools.command.install.install, plugins)


if __name__ == '__main__':
    unittest.main()
