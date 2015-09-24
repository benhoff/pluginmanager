from simpleyapsy.iplugin import IPlugin

class IsSubclass(object):
    def __init__(self, klass=IPlugin):
        self.klass = klass

    def is_valid(self, module_attribute):
        valid = False
        if issubclass(module_attribute, self.klass):
            valid = True

        return valid
