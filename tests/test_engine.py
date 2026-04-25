import unittest

from smart_indent_engine import format_text
from smart_indent_languages import detect_language, is_language_allowed


class DetectionTests(unittest.TestCase):
    def test_detect_by_extension(self):
        self.assertEqual(detect_language("index.tsx", None), "tsx")

    def test_detect_by_syntax(self):
        self.assertEqual(detect_language(None, "Packages/Python/Python.sublime-syntax"), "python")


class EngineTests(unittest.TestCase):

    def test_vue_template_tags_indent_like_html(self):
        source = "<template>\n<div>\n<span>Hello</span>\n</div>\n</template>\n"
        expected = "<template>\n    <div>\n        <span>Hello</span>\n    </div>\n</template>\n"
        self.assertEqual(format_text(source, "vue", "    "), expected)

    def test_vue_script_block_uses_javascript_indentation(self):
        source = "<script>\nif (ready) {\nconsole.log('ok')\n}\n</script>\n"
        expected = "<script>\n    if (ready) {\n        console.log('ok')\n    }\n</script>\n"
        self.assertEqual(format_text(source, "vue", "    "), expected)

    def test_js_braces(self):
        source = "function x(){\nif(true){\nconsole.log('ok')\n}\n}\n"
        expected = "function x(){\n    if(true){\n        console.log('ok')\n    }\n}\n"
        self.assertEqual(format_text(source, "javascript", "    "), expected)

    def test_css_id_selector_keeps_hash_for_indentation(self):
        source = "#app {\ncolor: red;\n}\n"
        expected = "#app {\n    color: red;\n}\n"
        self.assertEqual(format_text(source, "css", "    "), expected)

    def test_javascript_private_field_keeps_hash_for_indentation(self):
        source = "class X {\n#config = {\nenabled: true\n}\n}\n"
        expected = "class X {\n    #config = {\n        enabled: true\n    }\n}\n"
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

    def test_html_style_block_uses_css_indentation(self):
        source = "<style>\n.card {\ncolor: red;\n}\n</style>\n"
        expected = "<style>\n    .card {\n        color: red;\n    }\n</style>\n"
        self.assertEqual(format_text(source, "html", "    "), expected)

    def test_html_script_block_uses_javascript_indentation(self):
        source = "<script>\nif (ready) {\nconsole.log('ok')\n}\n</script>\n"
        expected = "<script>\n    if (ready) {\n        console.log('ok')\n    }\n</script>\n"
        self.assertEqual(format_text(source, "html", "    "), expected)

    def test_jsx_tags_indent_like_html(self):
        source = "<div>\n<span>Hello</span>\n</div>\n"
        expected = "<div>\n    <span>Hello</span>\n</div>\n"
        self.assertEqual(format_text(source, "jsx", "    "), expected)

    def test_tsx_nested_tags_indent_like_html(self):
        source = "<section>\n<div>\nText\n</div>\n</section>\n"
        expected = "<section>\n    <div>\n        Text\n    </div>\n</section>\n"
        self.assertEqual(format_text(source, "tsx", "    "), expected)

    def test_jsx_self_closing_tag_does_not_increase_depth(self):
        source = "<div>\n<img src=\"x.png\" />\n<span>Caption</span>\n</div>\n"
        expected = "<div>\n    <img src=\"x.png\" />\n    <span>Caption</span>\n</div>\n"
        self.assertEqual(format_text(source, "jsx", "    "), expected)

    def test_markdown_code_fence_preserved(self):
        source = "- item\n```js\nfunction x(){\nreturn 1\n}\n```\n"
        expected = "- item\n```js\nfunction x(){\nreturn 1\n}\n```\n"
        self.assertEqual(format_text(source, "markdown", "  "), expected)

    def test_fallback_plain_text(self):
        source = "hello\nworld\n"
        self.assertEqual(format_text(source, "text", "    "), source)

    def test_json_nested_objects_and_arrays(self):
        source = "{\n\"users\": [\n{\n\"name\": \"Ada\"\n}\n]\n}\n"
        expected = "{\n    \"users\": [\n        {\n            \"name\": \"Ada\"\n        }\n    ]\n}\n"
        self.assertEqual(format_text(source, "json", "    "), expected)

    def test_html_comment_does_not_change_depth(self):
        source = "<div>\n<!-- comment -->\n<span>Text</span>\n</div>\n"
        expected = "<div>\n    <!-- comment -->\n    <span>Text</span>\n</div>\n"
        self.assertEqual(format_text(source, "html", "    "), expected)

    def test_python_elif_and_else_dedent(self):
        source = "if x:\nprint(1)\nelif y:\nprint(2)\nelse:\nprint(3)\n"
        expected = "if x:\n    print(1)\nelif y:\n    print(2)\nelse:\n    print(3)\n"
        self.assertEqual(format_text(source, "python", "    "), expected)

    def test_markdown_nested_list_indentation(self):
        source = "- parent\n  - child\n- sibling\n"
        expected = "- parent\n  - child\n- sibling\n"
        self.assertEqual(format_text(source, "markdown", "  "), expected)


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
