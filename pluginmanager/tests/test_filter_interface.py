import unittest
from pluginmanager import PluginInterface


class TestObj:
    pass


class TestFilterInterface(unittest.TestCase):
    def setUp(self):
        interface = PluginInterface()
        self.interface = interface.get_filter_interface()

    def test_interface(self):
        # all methods in interface follow this pattern
        template = '{}_{}_filters'
        # currently the only two filters supported are file and module
        filters = ['file', 'module']
        # set up a function to get the actual method calls
        get_func = lambda attr: getattr(self.interface, attr)
        # list comprhensions, our function, and filters to get all the methods
        adders = [get_func(template.format('add',
                                           filter_)) for filter_ in filters]

        setters = [get_func(template.format('set',
                                            filter_)) for filter_ in filters]

        getters = [get_func(template.format('get',
                                            filter_)) for filter_ in filters]

        removers = [get_func(template.format('remove',
                                             filter_)) for filter_ in filters]
        instance = TestObj()
        second_instance = TestObj()
        for adder, setter, getter, remover in zip(adders, setters,
                                                  getters, removers):

            adder(instance)
            self.assertIn(instance, getter())
            setter(second_instance)
            self.assertIn(second_instance, getter())
            self.assertNotIn(instance, getter())
            remover(second_instance)
            self.assertNotIn(second_instance, getter())
