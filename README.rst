pluginmanager
=============

|Build Status| |Coverage Status| |Code Climate|

python plugin management, simplified.

::

    from pluginmanager import Interface

    plugin_interface = Interface()
    plugin_interface.set_plugin_directories('my/fancy/plugin/path')
    plugins = plugin_interface.collect_plugins()

Library currently under heavy development and may not be ready for use

Installation
------------

::

    pip install pluginmanager

-or-

::

    pip install git+https://github.com/benhoff/pluginmanager.git

.. |Build Status| image:: https://travis-ci.org/benhoff/pluginmanager.svg?branch=master
    :target: https://travis-ci.org/benhoff/simpleyapsy
.. |Coverage Status| image:: https://coveralls.io/repos/benhoff/pluginmanager/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/benhoff/pluginmanager?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/benhoff/pluginmanager/badges/gpa.svg
    :target: https://codeclimate.com/github/benhoff/pluginmanager
