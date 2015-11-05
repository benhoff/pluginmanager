import sys

try:
    from site import getsitepackages
except ImportError:
    # getsitepackages is broken with virtualenvs
    # https://github.com/pypa/virtualenv/issues/355
    from distutils.sysconfig import get_python_lib as getsitepackages

_ver = sys.version_info

is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)

if is_py2:
    import imp
    load_source = imp.load_source
if is_py3:
    if _ver[1] >= 4:
        # flake8: noqa
        from importlib import reload
        import importlib

        def load_source(name, file_path):
            spec = importlib.util.spec_from_file_location(name,
                                                          file_path)
            module = spec.loader.load_module()
            return module
    else:
        # flake8: noqa
        from imp import reload
        import imp
        load_source = imp.load_source
