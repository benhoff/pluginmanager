# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Added
- Changelog!
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
