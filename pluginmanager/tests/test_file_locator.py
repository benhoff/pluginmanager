import unittest
from pluginmanager.file_manager import FileManager


class TestClass:
    pass


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()

    def test_set_file_filters(self):
        current_file_filters = self.file_manager.file_filters[0]
        # Create a abstract object for testing
        obj = TestClass()
        self.file_manager.set_file_filters(obj)
        self.assertNotIn(current_file_filters, self.file_manager.file_filters)
        self.assertIn(obj, self.file_manager.file_filters)

    def test_add_file_filters(self):
        test_obj = TestClass()
        self.file_manager.add_file_filters(test_obj)
        self.assertIn(test_obj, self.file_manager.file_filters)


if __name__ == '__main__':
    unittest.main()
