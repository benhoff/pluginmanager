# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
 - Nothing!
 
## [0.3.2]
### Added
- Entry Point Manager!
- Class documentation for PluginInterface

## [0.3.1]
### Added
- Method documentation to PluginInterface
- `except_blacklisted` method argument to add/set plugin filepaths methods in PluginInterface. This argument was present in the underlying method call, but had not been implemented in PluginInterface yet.
- `remove_from_stored` method argument to the add/set blacklisted filepaths in PluginInterface. This argument was again, present in the underlying method call, but had not been implemented in PluginInterface.

### Changed
- Removed `auto_manage_state` variable from PluginInterface initialization. The method call `collect_plugins` now has a `store_collected_plugins` boolean argument which tells the class whether to make the PluginInterface instance track the plugins state or not. Default is `True`.
- Method argument for PluginInterface.get_file_filters from `file_function` to `filter_function`.
- FileManager changes all paths to absolute paths in method calls involving filepaths.
- Method documentation in FileManager, DirectoryManager, PluginManager

### Fixed
- Previous wheel packages accidently included tests. Moved tests to the project root and fixed setup.py to not include tests and also automatically remove the egg package to ensure that no previous state gets bundled in the wheel packages.

## [0.3.0]
### Added
- Method documentation for `ModuleManager` and `PluginManager`
- `plugins` and `blacklisted_plugins` arguments to `PluginManager` initialization call.
- checks to make sure that plugins have `activate` methods before trying to call the `activate` method using the `activate_plugins` method in `PluginManager`

### Changed
- `module_filters` to be `module_plugin_filters` in `ModuleManager` and `PluginInterface`. This is a API change which affects the method calls in both classes.
- Moved `PLUGIN_FORBIDDEN_NAME` from the init file in file_filters to being defined in it's own file. The linter was throwing a hissy fit about it being defined in the init file.

### Removed
- `except_blacklisted` method argument from `add_site_packages_paths` in `DirectoryManager`. If the site packages path is blacklisted, shouldn't use this method.

## [0.2.2]
### Added
- Method documentaiton for `ModuleManager`

### Changed
- `ModuleManager` no longer has support for blacklisted filepaths. This was not used by the default implementation in `PluginInterface` as `FileManager` handles the blacklisting for the package. Initializer call no longer allows a `blacklisted_filepaths` option and the blacklist methods were removed.
