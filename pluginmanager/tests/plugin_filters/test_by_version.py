import unittest
from simpleyapsy.plugin_filters import by_version


class TestVersion(object):
    def __init__(self, version=None):
        self.version = version


class TestByVersion(unittest.TestCase):
    def setUp(self):
        self.version_1 = TestVersion(1.0)
        self.version_2 = TestVersion(2.0)
        self.version_none = TestVersion()
        self.plugins = [self.version_1, self.version_2, self.version_none]

    def test_min_version(self):
        plugins = by_version(self.plugins, min_version=2.0)
        self.assertIn(self.version_2, plugins)
        self.assertNotIn(self.version_1, plugins)
        self.assertNotIn(self.version_none, plugins)

    def test_max_version(self):
        plugins = by_version(self.plugins, max_version=1.0)
        self.assertIn(self.version_1, plugins)
        self.assertNotIn(self.version_2, plugins)
        self.assertNotIn(self.version_none, plugins)
