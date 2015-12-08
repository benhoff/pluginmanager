pluginmanager
=============

|Build Status| |Coverage Status| |Code Climate|

python plugin management, simplified.


https://github.com/benhoff/pluginmanager

Library under development. Contains rough edges/unfinished functionality. API subject to changes.

Installation
------------

::
    pip install pluginmanager

-or-

::
    pip install git+https://github.com/benhoff/pluginmanager.git
 
Quickstart
----------

::
    from pluginmanager import PluginInterface

    plugin_interface = PluginInterface()
    plugin_interface.set_plugin_directories('my/fancy/plugin/path')
    plugin_interface.collect_plugins()

    plugins = plugin_interface.get_instances()
   
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

::
    import pluginmanager
    
    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.add_plugins(YourCustomClassHere)
    
    plugins = plugin_interface.get_instances()

Alternatively, add instances.

::
    import pluginmanager
    
    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.add_plugins(your_instance_here)
    
    plugins = plugin_interface.get_instances()

pluginmanager is defaulted to automatically instantiate unique instances. 

Disable automatic instantiation.

::
    import pluginmanager
    
    plugin_interface = pluginmanager.PluginInterface()
    plugin_manager = plugin_interface.plugin_manager

    plugin_manager.instantiate_classes = False

Disable uniquness (Only one instance of class per pluginmanager)

::
    import pluginmanager
    
    plugin_interface = pluginmanager.PluginInterface()
    plugin_manager = plugin_interface.plugin_manager

    plugin_manager.unique_instances = False

Filter Instances
----------------

Pass in a class to get back just the instances of a class

::
    import pluginmanager
    
    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.set_plugin_directories('my/fancy/plugin/path')
    plugin_interface.collect_plugins()
    
    all_instances_of_class = plugin_interface.get_instances(MyPluginClass)

Alternatively, create and pass in your own custom filters.

::
    def custom_filter(plugins):
        result = []
        for plugin in plugins:
            if plugin.name == 'interesting name':
                result.append(plugin)
        return result
    
    filtered_plugins = plugin_interface.get_instances(custom_filter)

    class FilterWithState(object):
        def __init__(self, name):
            self.stored_name = name 

        def __call__(self, plugins):
            result = []
            for plugin in plugins:
                if plugin.name == self.stored_name:
                    result.append(plugin)
            return result

Architecture
------------
pluginmanager was designed to be as extensible as possible while also being easy to use. There are three layers of access.

:Interfaces: public facing
:Managers: extended or replaced
:Filters: implementation specific

Interface
----------
An interface was used to provide a simple programmer interface while maintaining the ability to separate out the concerns of the implementation. The main interface is the PluginInterface. PluginInterface is designed to be as stateless as possible, and have interjectable options where applicable.
 

Managers
--------
There are four managers which make up the core of the library.

:DirectoryManager: Maintains directory state. Responsbile for recursively searching through directories
:FileManager: Can maintain filepath state. Does maintain file filter state. Responsible for applying file filters to filepaths passed gotten from directories
:ModuleManager: Loads modules from source code. Keeps track of loaded modules. Maintains module filter state. Responsible for applying module filters to modules to get out plugins.
:PluginManager: Instantiates plugins. Maintains plugin state.


Filters
-------
Filters are designed to offer implementation-level extensiblity.
Want to only return only files start with "plugin"? Create a filter for it. Or use some of the provided filters to provide the desired implementation.

All filters are callable.

.. |Build Status| image:: https://travis-ci.org/benhoff/pluginmanager.svg?branch=master
    :target: https://travis-ci.org/benhoff/pluginmanager
.. |Coverage Status| image:: https://coveralls.io/repos/benhoff/pluginmanager/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/benhoff/pluginmanager?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/benhoff/pluginmanager/badges/gpa.svg
    :target: https://codeclimate.com/github/benhoff/pluginmanager
