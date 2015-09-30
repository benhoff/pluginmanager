import os
import sys


def get_module_name(filepath):
    if filepath.endswith('__init__.py'):
        name = os.path.dirname(filepath)
    else:
        name = os.path.splitext(os.path.basename(filepath))[0]
    return name


def create_unique_module_name(plugin_info_or_name):
    # get name
    # check to see if dict, else assume filepath
    if isinstance(plugin_info_or_name, dict):
        name = plugin_info_or_name['name']
    else:
        name = plugin_info_or_name

    module_template = 'yapsy_plugin_{name}'.format(name)
    module_template += '_{number}'
    number = 0
    while True:
        module_name = module_template.format(number)
        if module_name not in sys.modules:
            break
        number += 1

    return module_name
