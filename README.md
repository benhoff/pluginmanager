# pluginmanager
[![Build Status](https://travis-ci.org/benhoff/pluginmanager.svg?branch=master)](https://travis-ci.org/benhoff/simpleyapsy) [![Coverage Status](https://coveralls.io/repos/benhoff/pluginmanager/badge.svg?branch=master&service=github)](https://coveralls.io/github/benhoff/pluginmanager?branch=master) [![Code Climate](https://codeclimate.com/github/benhoff/pluginmanager/badges/gpa.svg)](https://codeclimate.com/github/benhoff/pluginmanager)

python plugin management, simplified.

	from pluginmanager import Interface
	
	plugin_interface = Interface()
	plugin_interface.set_plugin_directories('my/fancy/plugin/path')
	# plugins returns both classes and functions
	plugins = plugin_interface.collect_plugins()
	# plugin instances are instances of a class	
	plugin_instances = plugin_interface.get_instances()

Library currently under heavy development

### Installation
	pip install git+https://github.com/benhoff/pluginmanager.git

API is currently too unstable to push to PyPi at this time
