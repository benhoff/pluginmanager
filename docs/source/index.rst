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
    print(plugins) # doctest: +SKIP

.. testoutput:: quickstart
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
    print(plugins) # doctest +SKIP

.. testoutput:: manual_plugins
    
    [<CustomClass object at 0x...]

Alternatively, add instances.

::

    import pluginmanager
    
    plugin_interface = pluginmanager.PluginInterface()
    plugin_interface.add_plugins(your_instance_here)
    
    plugins = plugin_interface.get_instances()
.. toctree::
   :maxdepth: 2



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

