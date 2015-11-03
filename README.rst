pluginmanager
=============

|Build Status| |Coverage Status| |Code Climate|

python plugin management, simplified.

::

    from pluginmanager import PluginInterface

    plugin_interface = PluginInterface()
    plugin_interface.set_plugin_directories('my/fancy/plugin/path')
    plugin_interface.collect_plugins()

    plugins = plugin_interface.get_instances()

Library currently under heavy development and may not be ready for use

Installation
------------

::

    pip install pluginmanager

-or-

::

    pip install git+https://github.com/benhoff/pluginmanager.git

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
