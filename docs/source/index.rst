.. pluginmanager documentation master file, created by
   sphinx-quickstart on Wed Dec  9 22:32:56 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. testsetup:: quickstart

    import os
    from pluginmanager.tests.compat import tempfile
    tempdirectory = tempfile.TemporaryDirectory()
    plugin_directory_path = tempdirectory.name
    path = os.path.join(tempdirectory.name, 'test.py')
    with open(path, 'w+') as f:
        f.write('from pluginmanager import IPlugin\nclass Test(IPlugin):\n    pass')

pluginmanager
=============
|Build Status| |Coverage Status| |Code Climate|

python plugin management, simplified.

`Source Code <https://github.com/benhoff/pluginmanager>`_

Library under development. Contains rough edges/unfinished functionality. API subject to changes.

Installation
------------

::

    pip install pluginmanager

-or- ::

    pip install git+https://github.com/benhoff/pluginmanager.git

Quickstart
----------

.. testcode:: quickstart

    from pluginmanager import PluginInterface

    plugin_interface = PluginInterface()
    plugin_interface.set_plugin_directories(plugin_directory_path)
    plugin_interface.collect_plugins() # doctest: +SKIP

    plugins = plugin_interface.get_instances()
    print(plugins) # doctest: +SKIP +HIDE

.. testoutput:: quickstart
    :hide:
    :options: +ELLIPSIS

    [<pluginmanager_plugin_test_0.Test object at 0x...]

Custom Plugins
--------------

The quickstart will only work if you subclass `IPlugin` for your custom plugins.

::

    import pluginmanager

    class MyCustomPlugin(pluginmanager.IPlugin):
        def __init__(self):
            self.name = 'custom_name'
            super().__init__()

Or register your class as subclass of IPlugin.

::

    import pluginmanager

    pluginmanager.IPlugin.register(YourClassHere)

Add Plugins Manually
--------------------
Add classes.

.. testcode:: manual_plugins

    import pluginmanager

    class CustomClass(pluginmanager.IPlugin):
        pass

    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.add_plugins(CustomClass)

    plugins = plugin_interface.get_instances()
    print(plugins) # doctest: +SKIP

.. testoutput:: manual_plugins
    :hide:

    [<CustomClass object at 0x...]

Alternatively, add instances.

.. testcode:: manual_plugins

    import pluginmanager

    class CustomClass(pluginmanager.IPlugin):
        pass

    custom_class_instance = CustomClass()

    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.add_plugins(custom_class_instance)

    plugins = plugin_interface.get_instances()
    print(plugins) # doctest: +SKIP

.. testoutput:: manual_plugins
    :hide:

    [<CustomClass object at 0x...]

pluginmanager is defaulted to automatically instantiate unique instances. Disable automatic instantiation.

::

    import pluginmanager

    plugin_interface = pluginmanager.PluginInterface()
    plugin_manager = plugin_interface.plugin_manager

    plugin_manager.instantiate_classes = False

Disable uniqueness (Only one instance of class per pluginmanager)

::

    import pluginmanager

    plugin_interface = pluginmanager.PluginInterface()
    plugin_manager = plugin_interface.plugin_manager

    plugin_manager.unique_instances = False

Filter Instances
----------------

Pass in a class to get back just the instances of a class

.. testcode:: filter_instances

    import pluginmanager

    class MyPluginClass(pluginmanager.IPlugin):
        pass

    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.add_plugins(MyPluginClass)

    all_instances_of_class = plugin_interface.get_instances(MyPluginClass)
    print(all_instances_of_class) # doctest: +SKIP

.. testoutput:: filter_instances
    :hide:

    [<MyPluginClass object at 0x...]

Alternatively, create and pass in your own custom filters. Either make a class based filter

.. testcode:: filter_instances

    # create a custom plugin class
    class Plugin(pluginmanager.IPlugin):
        def __init__(self, name):
            self.name = name

    # create a custom filter
    class NameFilter(object):
        def __init__(self, name):
            self.stored_name = name 

        def __call__(self, plugins):
            result = []
            for plugin in plugins:
                if plugin.name == self.stored_name:
                    result.append(plugin)
            return result

    # create an instance of our custom filter
    mypluginclass_name_filter = NameFilter('good plugin')

    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.add_plugins([Plugin('good plugin'), 
                                  Plugin('bad plugin')])

    filtered_plugins = plugin_interface.get_instances(mypluginclass_name_filter)
    print(filtered_plugins[0].name) # doctest: +SKIP

.. testoutput:: filter_instances
    :hide:

    good plugin

Or make a function based filter

.. testcode:: filter_instances

    # create a custom plugin class
    class Plugin(pluginmanager.IPlugin):
        def __init__(self, name):
            self.name = name

    # create a function based filter
    def custom_filter(plugins):
        result = []
        for plugin in plugins:
            if plugin.name == 'good plugin':
                result.append(plugin)
        return result

    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.add_plugins([Plugin('good plugin'), 
                                  Plugin('bad plugin')])

    filtered_plugins = plugin_interface.get_instances(mypluginclass_name_filter)
    print(filtered_plugins[0].name)

.. testoutput:: filter_instances
    :hide:

    good plugin

.. toctree::
   :maxdepth: 2

   code_ref/index.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |Build Status| image:: https://travis-ci.org/benhoff/pluginmanager.svg?branch=master
    :target: https://travis-ci.org/benhoff/pluginmanager
.. |Coverage Status| image:: https://coveralls.io/repos/benhoff/pluginmanager/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/benhoff/pluginmanager?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/benhoff/pluginmanager/badges/gpa.svg
    :target: https://codeclimate.com/github/benhoff/pluginmanager

    

.. testcleanup::
    tempdirectory.cleanup()

