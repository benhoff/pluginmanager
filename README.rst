pluginmanager
=============

|Build Status| |Coverage Status| |Code Climate|

python plugin management, simplified.

Library under development and contains rough edges/unfinished functionality. While not anticipated, API may be subject to changes.

Quickstart
----------

::

    from pluginmanager import PluginInterface

    plugin_interface = PluginInterface()
    plugin_interface.set_plugin_directories('my/fancy/plugin/path')
    plugin_interface.collect_plugins()

    plugins = plugin_interface.get_instances()


Installation
------------

::

    pip install pluginmanager

-or-

::

    pip install git+https://github.com/benhoff/pluginmanager.git
    
Custom Plugins
--------------

The quickstart will only work if you subclass `IPlugin` for your custom plugins (or register your custom class with `IPlugin`, or use the 'get_plugins' method on `PluginInterface`.)

::

    import pluginmanager
    class MyCustomPlugin(pluginmanager.IPlugin):
        pass

`IPlugin` comes with three instance variables: active: bool, configuration: dict, name: str

and one class variable: CONFIGURATION_TEMPLATE: dict

At the very least, you should give your custom implementations a 'name'. If a name is not given and the parent class initializer is called, a name will be written to the instance if the attribute doesn't exist. FYI.

IPlugin has 5 methods: activate, deactivate, get_configuration_template, check_configuration, and configure

Reimplement (or not) as needed.

If the default implementation of IPlugin doesn't fit your needs, register your class as subclass of IPlugin.

::

    IPlugin.register(YourClassHere)

Architecture
------------
pluginmanager was designed to be as extensible as possible while also being easy to use. There are three layers of access.

:Interfaces: public facing
:Managers: extended or replaced
:Filters: implementation specific

Interfaces
----------
Interfaces were used to provide a simple programmer interface while maintaining the ability to separate out the concerns of the implementation. The main interface is the PluginInterface, which is designed to be as stateless as possible, and have interjectable options, where applicable.

PluginInterface provides the cability to instantiate two other interfaces, the BlacklistInterface and FilterInterface. These interfaces provide universal access to the blacklisting (selectively implemented) and filtering APIs respectively. 

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

NOTE: Final implementation of filters and how they interact with the library is currently a WIP and should be considered unstable.

.. |Build Status| image:: https://travis-ci.org/benhoff/pluginmanager.svg?branch=master
    :target: https://travis-ci.org/benhoff/pluginmanager
.. |Coverage Status| image:: https://coveralls.io/repos/benhoff/pluginmanager/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/benhoff/pluginmanager?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/benhoff/pluginmanager/badges/gpa.svg
    :target: https://codeclimate.com/github/benhoff/pluginmanager
