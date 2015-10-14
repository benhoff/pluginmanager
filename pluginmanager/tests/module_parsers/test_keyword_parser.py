import types
import unittest

from simpleyapsy.module_parsers import KeywordParser


class TestKeywordParser(unittest.TestCase):
    def setUp(self):
        self.module_parser = KeywordParser()

    def test_get_plugin(self):
        keyword = self.module_parser.keywords[0]
        test_module = types.ModuleType("TestModule")
        test_obj = type('', (), {})
        set_plugins = [test_obj]
        setattr(test_module, keyword, set_plugins)
        plugins = self.module_parser.get_plugins(test_module)
        self.assertIn(test_obj, plugins)
