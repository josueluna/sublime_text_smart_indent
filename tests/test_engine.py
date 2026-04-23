import unittest

from smart_indent_engine import format_text
from smart_indent_languages import detect_language, is_language_allowed


class DetectionTests(unittest.TestCase):
    def test_detect_by_extension(self):
        self.assertEqual(detect_language("index.tsx", None), "tsx")

    def test_detect_by_syntax(self):
        self.assertEqual(detect_language(None, "Packages/Python/Python.sublime-syntax"), "python")


class EngineTests(unittest.TestCase):
    def test_js_braces(self):
        source = "function x(){\nif(true){\nconsole.log('ok')\n}\n}\n"
        expected = "function x(){\n    if(true){\n        console.log('ok')\n    }\n}\n"
        self.assertEqual(format_text(source, "javascript", "    "), expected)

    def test_python_blocks(self):
        source = "def x():\nif True:\nreturn 1\n"
        expected = "def x():\n    if True:\n        return 1\n"
        self.assertEqual(format_text(source, "python", "    "), expected)

    def test_html_tags(self):
        source = "<div>\n<span>hello</span>\n</div>\n"
        expected = "<div>\n    <span>hello</span>\n</div>\n"
        self.assertEqual(format_text(source, "html", "    "), expected)

    def test_html_void_tag_no_extra_depth(self):
        source = "<div>\n<img src='x.png'>\n<p>caption</p>\n</div>\n"
        expected = "<div>\n    <img src='x.png'>\n    <p>caption</p>\n</div>\n"
        self.assertEqual(format_text(source, "html", "    "), expected)

    def test_markdown_code_fence_preserved(self):
        source = "- item\n```js\nfunction x(){\nreturn 1\n}\n```\n"
        expected = "- item\n```js\nfunction x(){\nreturn 1\n}\n```\n"
        self.assertEqual(format_text(source, "markdown", "  "), expected)


    def test_python_malformed_def_does_not_force_depth(self):
        source = "def maybe_broken\nprint('x')\n"
        expected = "def maybe_broken\nprint('x')\n"
        self.assertEqual(format_text(source, "python", "    "), expected)

    def test_js_string_braces_are_ignored(self):
        source = "function x(){\nconsole.log(\"{\")\n}\n"
        expected = "function x(){\n    console.log(\"{\")\n}\n"
        self.assertEqual(format_text(source, "javascript", "    "), expected)

    def test_fallback_plain_text(self):
        source = "hello\nworld\n"
        self.assertEqual(format_text(source, "text", "    "), source)


class FormatOnSaveAllowlistTests(unittest.TestCase):
    def test_none_allowlist_allows_all_languages(self):
        self.assertTrue(is_language_allowed("python", None))

    def test_empty_allowlist_allows_all_languages(self):
        self.assertTrue(is_language_allowed("markdown", []))

    def test_allowlist_filters_languages(self):
        self.assertTrue(is_language_allowed("python", ["python", "javascript"]))
        self.assertFalse(is_language_allowed("html", ["python", "javascript"]))

    def test_allowlist_is_case_insensitive(self):
        self.assertTrue(is_language_allowed("TypeScript", ["typescript"]))


if __name__ == "__main__":
    unittest.main()
