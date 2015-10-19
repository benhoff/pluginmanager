PLUGIN_FORBIDDEN_NAME = ';;'

from .with_info_file import WithInfoFileGetter
from .matching_regex import MatchingRegexFileGetter
from .filenames import FilenameFileGetter

__all__ = ["WithInfoFileGetter",
           "MatchingRegexFileGetter",
           "FilenameFileGetter"]
