# simpleyapsy
python plugin management, simplified.

    from simpleyapsy import Interface
    
    plugin_manager = Interface()
    plugin_manager.set_plugin_locations('my/fancy/plugin/path')
    plugins = plugin_manager.get_plugins()
    # Work with plugins here

Library currently under heavy development

### Installation
    pip install git+https://github.com/benhoff/simpleyapsy.git

API is currently too unstable to push to PyPi at this time
