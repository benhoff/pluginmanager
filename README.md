# simpleyapsy
[![Build Status](https://travis-ci.org/benhoff/simpleyapsy.svg?branch=master)](https://travis-ci.org/benhoff/simpleyapsy) [![Coverage Status](https://coveralls.io/repos/benhoff/simpleyapsy/badge.svg?branch=master&service=github)](https://coveralls.io/github/benhoff/simpleyapsy?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/de59c9e951c8464aae28a4cba227a5e6)](https://www.codacy.com/app/hoff-benjamin-k/simpleyapsy)

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
