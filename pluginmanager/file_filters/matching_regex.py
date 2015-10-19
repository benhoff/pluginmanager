import os
import re


class MatchingRegexFileFilter(object):
    """
    An analyzer that targets plugins decribed by files whose
    name match a given regex.
    """
    def __init__(self, regexp):
        if not isinstance(regexp, list):
            regexp = [regexp]
        regex_expressions = []
        for regex in regexp:
            regex_expressions.append(re.compile(regex))
        self.regex_expressions = regex_expressions

    def __call__(self, filepaths):
        plugin_filepaths = []
        for filepath in filepaths:
            if self.plugin_valid(filepath):
                plugin_filepaths.append(filepath)
        return plugin_filepaths

    def set_regex_expressions(self, regex_expressions):
        if not isinstance(regex_expressions, list):
            regex_expressions = [regex_expressions]
        self.regex_expressions = regex_expressions

    def add_regex_expressions(self, regex_expressions):
        if not isinstance(regex_expressions, list):
            regex_expressions = [regex_expressions]
        self.regex_expressions.extend(regex_expressions)

    def plugin_valid(self, filename):
        """
        Checks if the given filename is a valid plugin for this Strategy
        """
        filename = os.path.basename(filename)
        for regex in self.regex_expressions:
            if regex.match(filename):
                return True
        return False
