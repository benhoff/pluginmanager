import unittest
from pluginmanager.file_locator import FileLocator


class TestClass:
    pass


class TestFileLocator(unittest.TestCase):
    def setUp(self):
        self.file_locator = FileLocator()

    def test_set_file_getters(self):
        current_file_getters = self.file_locator.file_getters[0]
        # Create a abstract object for testing
        obj = TestClass()
        self.file_locator.set_file_getters(obj)
        self.assertNotIn(current_file_getters, self.file_locator.file_getters)
        self.assertIn(obj, self.file_locator.file_getters)

    def test_add_file_getters(self):
        test_obj = TestClass()
        self.file_locator.add_file_getters(test_obj)
        self.assertIn(test_obj, self.file_locator.file_getters)


if __name__ == '__main__':
    unittest.main()
