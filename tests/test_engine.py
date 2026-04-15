import unittest

from smart_indent_engine import format_text
from smart_indent_languages import detect_language


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

    def test_fallback_plain_text(self):
        source = "hello\nworld\n"
        self.assertEqual(format_text(source, "text", "    "), source)


if __name__ == "__main__":
    unittest.main()
