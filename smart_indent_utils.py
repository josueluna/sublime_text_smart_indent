"""Utility helpers for smart indentation plugin."""

from __future__ import annotations


def get_indent_unit(translate_tabs_to_spaces=True, tab_size=4):
    """Return indent unit based on view settings."""
    if translate_tabs_to_spaces:
        return " " * max(int(tab_size or 4), 1)
    return "\t"


def line_indent_depth(line, indent_unit):
    """Estimate indentation depth for a line."""
    if not line.strip():
        return 0

    if indent_unit == "\t":
        return len(line) - len(line.lstrip("\t"))

    leading = len(line) - len(line.lstrip(" "))
    size = len(indent_unit)
    return int(leading / size) if size else 0


def clamp_depth(depth):
    return max(depth, 0)
