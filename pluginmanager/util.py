import os
import sys


def to_absolute_paths(paths):
    """
    helper method to change `paths` to absolute paths.
    Returns a `set` object
    `paths` can be either a single object or iterable
    """
    abspath = os.path.abspath
    paths = return_set(paths)
    absolute_paths = {abspath(x) for x in paths}
    return absolute_paths


def get_module_name(filepath):
    if filepath.endswith('__init__.py'):
        name = os.path.basename(os.path.dirname(filepath))
    else:
        name = os.path.splitext(os.path.basename(filepath))[0]
    return name


def remove_from_list(list, remove_items):
    list = return_list(list)
    remove_items = return_list(remove_items)
    for remove in remove_items:
        if remove in list:
            list.remove(remove)

    return list


def remove_from_set(set, remove_items):
    set = return_set(set)
    remove_items = return_set(remove_items)
    for item in remove_items:
        if item in set:
            set.remove(item)

    return set


def create_unique_module_name(plugin_info_or_name):
    # get name
    # check to see if dict, else assume filepath
    if isinstance(plugin_info_or_name, dict):
        name = plugin_info_or_name['name']
    else:
        name = plugin_info_or_name

    module_template = 'pluginmanager_plugin_{}'.format(name)
    module_template += '_{number}'
    number = 0
    while True:
        module_name = module_template.format(number=number)
        if module_name not in sys.modules:
            break
        number += 1

    return module_name


def get_filepaths_from_dir(dir_path):
    filepaths = []
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if os.path.isfile(filepath):
            filepaths.append(filepath)
    return filepaths


def return_list(object):
    if isinstance(object, set):
        return list(object)
    elif isinstance(object, tuple):
        return list(object)
    elif not isinstance(object, list):
        return [object]
    else:
        return object


def return_set(object):
    if isinstance(object, set):
        return object
    elif isinstance(object, (list, tuple)):
        return set(object)
    else:
        return set([object])
