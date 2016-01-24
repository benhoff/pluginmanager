from pluginmanager.compat import is_py2
import tempfile


if is_py2:
    # need to backport `tempfile.TemporaryDirectory`
    import shutil as _shutil
    import warnings as _warnings
    from tempfile import mkdtemp
    from ConfigParser import ConfigParser

    def read_dict(self, dictionary, source='<dict>'):
        elements_added = set()
        for section, keys in dictionary.items():
            section = str(section)
            try:
                self.add_section(section)
            except:
                pass
            elements_added.add(section)
            for key, value in keys.items():
                key = self.optionxform(str(key))
                if value is not None:
                    value = str(value)
                elements_added.add((section, key))
                self.set(section, key, value)
    ConfigParser.read_dict = read_dict
    FILE_ERROR = OSError

    class TemporaryDirectory(object):
        """Create and return a temporary directory.  This has the same
        behavior as mkdtemp but can be used as a context manager.  For
        example:

            with TemporaryDirectory() as tmpdir:
                ...

        Upon exiting the context, the directory and everything contained
        in it are removed.
        """

        def __init__(self, suffix='', prefix="tmp", dir=None):
            self.name = mkdtemp(suffix, prefix, dir)

        @classmethod
        def _cleanup(cls, name, warn_message):
            _shutil.rmtree(name)
            _warnings.warn(warn_message)

        def __repr__(self):
            return "<{} {!r}>".format(self.__class__.__name__, self.name)

        def __enter__(self):
            return self.name

        def __del__(self):
            try:
                self._cleanup(self.name,
                              warn_message="Implicitly cleaning up {!r}".format(self))  # noqa
            except (OSError, NameError):
                pass

        def __exit__(self, exc, value, tb):
            self.cleanup()

        def cleanup(self):
            _shutil.rmtree(self.name)

    tempfile.TemporaryDirectory = TemporaryDirectory
