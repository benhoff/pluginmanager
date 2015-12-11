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
    print(plugins)

.. testoutput:: quickstart 

    this should fail.

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

