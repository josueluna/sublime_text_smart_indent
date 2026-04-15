"""Language detection and lightweight syntax helpers."""

from __future__ import annotations

import os

_EXTENSION_TO_LANGUAGE = {
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".json": "json",
    ".py": "python",
    ".md": "markdown",
    ".markdown": "markdown",
    ".txt": "text",
}


def detect_language(file_name=None, syntax=None):
    """Detect language from extension first, then syntax name."""
    lang = "text"

    if file_name:
        _, ext = os.path.splitext(file_name.lower())
        if ext in _EXTENSION_TO_LANGUAGE:
            return _EXTENSION_TO_LANGUAGE[ext]

    syntax_name = (syntax or "").lower()
    if "html" in syntax_name:
        lang = "html"
    elif "css" in syntax_name:
        lang = "css"
    elif "typescript" in syntax_name and "tsx" in syntax_name:
        lang = "tsx"
    elif "tsx" in syntax_name:
        lang = "tsx"
    elif "typescript" in syntax_name:
        lang = "typescript"
    elif "jsx" in syntax_name:
        lang = "jsx"
    elif "javascript" in syntax_name:
        lang = "javascript"
    elif "json" in syntax_name:
        lang = "json"
    elif "python" in syntax_name:
        lang = "python"
    elif "markdown" in syntax_name:
        lang = "markdown"
    elif "plain text" in syntax_name:
        lang = "text"

    return lang
