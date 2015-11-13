import sys

try:
    from site import getsitepackages
except ImportError:
    # getsitepackages is broken with virtualenvs
    # https://github.com/pypa/virtualenv/issues/355
    from distutils.sysconfig import get_python_lib as getsitepackages

def with_metaclass(meta, *bases):
    """
    function from jinja2/_compat.py. License: BSD.

    Use it like this::

        class BaseForm(object):
            pass

        class FormType(type):
            pass

        class Form(with_metaclass(FormType, BaseForm)):
            pass
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})

_ver = sys.version_info

is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)

if is_py2:
    import imp
    load_source = imp.load_source
    reload = imp.reload
    FILE_ERROR = IOError
    from ConfigParser import ConfigParser
    def read_file(parser, source):
        return parser.readfp(source)
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

    ConfigParser.read_file = read_file
    ConfigParser.read_dict = read_dict

if is_py3:
    import builtins
    # Work around for python 3.2
    FILE_ERROR = getattr(builtins,
                         "FileNotFoundError",
                         getattr(builtins, "OSError"))
    from configparser import ConfigParser
    if _ver[1] >= 4:
        # flake8: noqa
        import importlib

        def load_source(name, file_path):
            spec = importlib.util.spec_from_file_location(name,
                                                          file_path)
            module = spec.loader.load_module()
            return module
    else:
        # flake8: noqa
        import imp
        load_source = imp.load_source
