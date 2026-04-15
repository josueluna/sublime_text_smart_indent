"""Sublime Text commands for smart indentation formatting."""

from __future__ import annotations

import sublime
import sublime_plugin

from smart_indent_engine import format_text
from smart_indent_languages import detect_language
from smart_indent_utils import get_indent_unit


PLUGIN_SETTINGS = "SmartIndent.sublime-settings"


def plugin_loaded():
    sublime.load_settings(PLUGIN_SETTINGS)


class SmartIndentFormatFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        settings = view.settings()

        if view.is_read_only():
            sublime.status_message("Smart Indent: file is read-only")
            return

        language = detect_language(view.file_name(), settings.get("syntax"))
        indent_unit = get_indent_unit(
            settings.get("translate_tabs_to_spaces", True),
            settings.get("tab_size", 4),
        )

        region = sublime.Region(0, view.size())
        original_text = view.substr(region)
        updated_text = format_text(original_text, language, indent_unit)

        if updated_text != original_text:
            view.replace(edit, region, updated_text)
            sublime.status_message("Smart Indent: formatted as {}".format(language))
        else:
            sublime.status_message("Smart Indent: no changes needed")


class SmartIndentAutoFormatOnSaveListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        package_settings = sublime.load_settings(PLUGIN_SETTINGS)
        if not package_settings.get("format_on_save", False):
            return

        # Avoid modifying command palette / quick panel / widget views.
        if view.settings().get("is_widget"):
            return

        view.run_command("smart_indent_format_file")
