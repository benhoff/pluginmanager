PLUGIN_FORBIDDEN_NAME = ';;'

from .with_info_file import WithInfoFileGetter
from .matching_regex import MatchingRegexFileGetter

__all__ = ["with_info_file", "matching_regex"]
