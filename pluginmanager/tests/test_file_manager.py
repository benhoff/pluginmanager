import os
import unittest
from .compat import tempfile
from pluginmanager.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        """
        Create the file manager, a temporary directory, and
        two empty files cleverly named `one.py` and `two.py`
        """
        self.file_manager = FileManager()
        self.temp_dir = tempfile.TemporaryDirectory()

        file_path_template = os.path.join(self.temp_dir.name, '{}.py')
        self.filepath_one = file_path_template.format('one')
        self.filepath_two = file_path_template.format('two')
        open(self.filepath_one, 'a+').close()
        open(self.filepath_two, 'a+').close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_collect_filepaths(self):
        """
        pass in the temporary directory in to the `collect_filepaths` method
        and then check to see if the filepaths created in the `setUp` function
        are present in the collected filepaths
        """
        filepaths = self.file_manager.collect_filepaths(self.temp_dir.name)
        self.assertIn(self.filepath_one, filepaths)
        self.assertIn(self.filepath_two, filepaths)

    def test_collect_filepaths_with_blacklisted_filepath(self):
        """
        add filepath_one to the blacklisted filepaths and then
        collect the filepaths and verify that filepath_one is NOT
        in the collected filepaths, but filepath_two is.
        """
        self.file_manager.add_blacklisted_filepaths(self.filepath_one)
        filepaths = self.file_manager.collect_filepaths(self.temp_dir.name)
        self.assertIn(self.filepath_two, filepaths)
        self.assertNotIn(self.filepath_one, filepaths)

    def test_add_plugin_filepaths(self):
        """
        Wnat to test the `except_blacklisted` arg to this method,
        so start off by adding a blacklisted filepath. Then add in
        both the blacklisted filepath and a non blacklisted filepath
        using the method call. Check to make sure that the blacklisted filepath
        is NOT added and that the normal filepath is. Then use the override
        method to add in the blacklisted file and see that it is tracked
        internally.
        """
        self.file_manager.add_blacklisted_filepaths(self.filepath_two)
        filepaths = [self.filepath_one, self.filepath_two]
        self.file_manager.add_plugin_filepaths(filepaths)
        self.assertIn(self.filepath_one, self.file_manager.plugin_filepaths)
        self.assertNotIn(self.filepath_two, self.file_manager.plugin_filepaths)

        self.file_manager.add_plugin_filepaths(self.filepath_two,
                                               except_blacklisted=False)

        self.assertIn(self.filepath_two, self.file_manager.plugin_filepaths)

    def test_set_plugin_filepaths(self):
        """
        Wnat to test the `except_blacklisted` arg to this method,
        so start off by adding a blacklisted filepath. Then set the filepaths
        to both the blacklisted filepath and a non blacklisted filepath
        using the method call. Check to make sure that the blacklisted filepath
        is NOT added and that the normal filepath is. Then use the override
        argument to set in the blacklisted file and see that it is tracked
        internally.
        """
        self.file_manager.add_blacklisted_filepaths(self.filepath_two)

        filepaths = [self.filepath_one, self.filepath_two]
        self.file_manager.set_plugin_filepaths(filepaths)
        self.assertIn(self.filepath_one, self.file_manager.plugin_filepaths)
        self.assertNotIn(self.filepath_two, self.file_manager.plugin_filepaths)

        self.file_manager.set_plugin_filepaths(self.filepath_two,
                                               except_blacklisted=False)

        self.assertIn(self.filepath_two, self.file_manager.plugin_filepaths)
        self.assertNotIn(self.filepath_one, self.file_manager.plugin_filepaths)

    def test_remove_plugin_filepaths(self):
        """
        Add in a filepath, make sure it's there, remove it, make sure it's not
        there.
        """
        self.file_manager.add_plugin_filepaths(self.filepath_one)
        self.assertIn(self.filepath_one, self.file_manager.plugin_filepaths)
        self.file_manager.remove_plugin_filepaths(self.filepath_one)
        self.assertNotIn(self.filepath_one, self.file_manager.plugin_filepaths)

    def test_get_plugin_filepaths(self):
        """
        get filepaths, assert that it is a set
        """
        filepaths = self.file_manager.get_plugin_filepaths()
        self.assertTrue(isinstance(filepaths, set))
        self.assertEqual(len(filepaths), 0)

    def test_set_file_filters(self):
        """
        create some old state to overwrite, then set the file filter
        to be an object and check to make sure the object is tracked
        in state
        """
        # create old state to be overwritten
        old_file_filter_state = object()
        self.file_manager.add_file_filters(old_file_filter_state)

        # Create a abstract object for testing
        obj = object()
        self.file_manager.set_file_filters(obj)
        self.assertNotIn(old_file_filter_state, self.file_manager.file_filters)
        self.assertIn(obj, self.file_manager.file_filters)

    def test_add_file_filters(self):
        """
        Create an object, add it to the file filters and assert that
        the created object is in the file filters
        check first that the file filters are empty
        """
        test_obj = object()
        self.assertEqual(len(self.file_manager.file_filters), 0)
        self.file_manager.add_file_filters(test_obj)
        self.assertIn(test_obj, self.file_manager.file_filters)

    def test_get_file_filters(self):
        """
        create two test objects and track them internally.
        Using the get method, return the internal state and make sure
        both test objects are in the internal state.

        want to test the optional argument `filter_function`.
        Therefore create a `test_filter` function and hardcode
        it to return one of the created objects.
        Pass in the created filter function in and make
        sure that it is called correctly.
        """
        obj_1 = object()
        obj_2 = object()
        self.file_manager.set_file_filters([obj_1, obj_2])
        filters = self.file_manager.get_file_filters()
        self.assertIn(obj_1, filters)
        self.assertIn(obj_2, filters)

        def test_filter(file_filters):
            for f in file_filters:
                if f == obj_1:
                    return [obj_1, ]

        result = self.file_manager.get_file_filters(test_filter)
        self.assertIn(obj_1, result)
        self.assertNotIn(obj_2, result)

    def test_remove_file_filters(self):
        """
        track a file filter than remove it. Make sure
        the removed filter is no longer tracked internally
        """
        test_filter = object()
        self.file_manager.add_file_filters(test_filter)
        self.assertIn(test_filter, self.file_manager.file_filters)

        self.file_manager.remove_file_filters(test_filter)
        self.assertNotIn(test_filter, self.file_manager.file_filters)

    def test_add_blacklisted_filepaths(self):
        """
        Want to check that we remove added blacklisted filepaths from stored
        plugin filepaths
        So at the start, add in our two filepaths to the internal state.

        assert that blacklisted filepaths are empty, then add a filepath.
        Assert that the added filepath is in the internal blacklist state and
        that the blacklisted filepath is NOT in the internal plugin filepath
        state.

        Next, overide the default arg for `remove_from_stored` to False, and
        add another blacklisted filepath. Now assert that the second
        blacklisted filepath is still tracked internally for a plugin filepath
        and that the blacklisted filepath is tracked as a blacklisted filepath
        """
        self.file_manager.add_plugin_filepaths([self.filepath_one,
                                                self.filepath_two])

        self.assertEqual(len(self.file_manager.blacklisted_filepaths), 0)
        self.file_manager.add_blacklisted_filepaths(self.filepath_one)
        self.assertIn(self.filepath_one,
                      self.file_manager.blacklisted_filepaths)

        self.assertNotIn(self.filepath_one, self.file_manager.plugin_filepaths)

        self.file_manager.add_blacklisted_filepaths(self.filepath_two,
                                                    remove_from_stored=False)

        self.assertIn(self.filepath_two,
                      self.file_manager.blacklisted_filepaths)

        self.assertIn(self.filepath_two,
                      self.file_manager.plugin_filepaths)

    def test_set_blacklisted_filepaths(self):
        """
        Want to check that we remove set blacklisted filepaths from stored
        plugin filepaths.
        So at the start, add in our two filepaths to the internal state.

        assert that blacklisted filepaths are empty, then set a blacklisted
        filepath. Assert that the set filepath is in the internal blacklist
        state and that the blacklisted filepath is NOT in the internal plugin
        filepath state.

        Next, overide the default arg for `remove_from_stored` to False, and
        set another blacklisted filepath. Now assert that the second
        blacklisted filepath is still tracked internally for a plugin filepath
        and that the blacklisted filepath is tracked as a blacklisted filepath
        """
        self.file_manager.add_plugin_filepaths([self.filepath_one,
                                                self.filepath_two])

        self.assertEqual(len(self.file_manager.blacklisted_filepaths), 0)
        self.file_manager.set_blacklisted_filepaths(self.filepath_one)
        self.assertIn(self.filepath_one,
                      self.file_manager.blacklisted_filepaths)

        self.assertNotIn(self.filepath_one, self.file_manager.plugin_filepaths)

        self.file_manager.set_blacklisted_filepaths(self.filepath_two,
                                                    remove_from_stored=False)

        self.assertIn(self.filepath_two,
                      self.file_manager.blacklisted_filepaths)

        self.assertIn(self.filepath_two, self.file_manager.plugin_filepaths)
        self.assertNotIn(self.filepath_one,
                         self.file_manager.blacklisted_filepaths)

    def test_remove_blacklisted_filepaths(self):
        """
        Add a blacklisted filepath, assert it is in the state.
        Then remove it using the method and assert that it is not in the state
        """
        self.file_manager.add_blacklisted_filepaths(self.filepath_one)
        self.assertIn(self.filepath_one,
                      self.file_manager.blacklisted_filepaths)

        self.file_manager.remove_blacklisted_filepaths(self.filepath_one)
        self.assertNotIn(self.filepath_one,
                         self.file_manager.blacklisted_filepaths)

    def test_get_blacklisted_filepath(self):
        """
        assert that return is set and is empty. Then add file and assert
        that the filepath is in the result and is a set object
        """
        blacklisted_filepath = self.file_manager.get_blacklisted_filepaths()
        self.assertTrue(isinstance(blacklisted_filepath, set))
        self.assertEqual(len(blacklisted_filepath), 0)
        self.file_manager.add_blacklisted_filepaths(self.filepath_one)

        tracked_filepaths = self.file_manager.get_blacklisted_filepaths()
        self.assertTrue(isinstance(tracked_filepaths, set))
        self.assertIn(self.filepath_one, tracked_filepaths)

    def test_filter_filepaths(self):
        filepaths = ['test/dir', 'dir/test']
        no_filter = self.file_manager._filter_filepaths(filepaths)
        self.assertEqual(filepaths, no_filter)

        def test_filter(filepaths):
            for filepath in filepaths:
                if filepath == 'test/dir':
                    filepath = [filepath]
                    return filepath

        self.file_manager.add_file_filters(test_filter)
        filtered_filepaths = self.file_manager._filter_filepaths(filepaths)
        self.assertIn('test/dir', filtered_filepaths)
        self.assertNotIn('dir/test', filtered_filepaths)


if __name__ == '__main__':
    unittest.main()
