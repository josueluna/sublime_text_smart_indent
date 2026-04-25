"""Rules-based indentation engine used by the Sublime command."""

from __future__ import annotations

import re

from smart_indent_utils import clamp_depth


_HTML_OPEN_TAG_RE = re.compile(r"<([a-zA-Z][\w:-]*)(\s[^>]*)?>")
_HTML_CLOSE_TAG_RE = re.compile(r"</([a-zA-Z][\w:-]*)>")
_HTML_SELF_CLOSING_RE = re.compile(r"<([a-zA-Z][\w:-]*)(\s[^>]*)?/>")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->")

_HTML_VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

PYTHON_DEDENT_PREFIXES = (
    "return",
    "raise",
    "break",
    "continue",
    "pass",
    "elif",
    "else",
    "except",
    "finally",
)


_DEF_OR_CLASS_RE = re.compile(r"^\s*(async\s+def|def|class)\s+")


def _sanitize_for_braces(line):
    """Remove quoted strings and single-line comments before brace counting."""
    stripped = re.sub(r"'(?:\\.|[^'\\])*'", "''", line)
    stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', stripped)

    # Basic single-line comment removal for common languages.
    stripped = re.sub(r"//.*$", "", stripped)
    return stripped


def _brace_delta(line):
    cleaned = _sanitize_for_braces(line)
    opens = cleaned.count("{") + cleaned.count("[") + cleaned.count("(")
    closes = cleaned.count("}") + cleaned.count("]") + cleaned.count(")")
    return opens - closes


def _line_starts_with_closer(line, language):
    stripped = line.lstrip()
    if language in ("html", "jsx", "tsx"):
        return bool(_HTML_CLOSE_TAG_RE.match(stripped))
    if language == "python":
        return _python_starts_dedent(stripped)
    return stripped.startswith(("}", "]", ")"))


def _html_delta(line):
    stripped = line.strip()
    if not stripped:
        return 0

    # Remove inline comments for tag analysis.
    working = _HTML_COMMENT_RE.sub("", stripped)
    if not working:
        return 0

    if _HTML_SELF_CLOSING_RE.search(working):
        return 0

    opens = 0
    for tag, _ in _HTML_OPEN_TAG_RE.findall(working):
        if tag.lower() not in _HTML_VOID_TAGS:
            opens += 1

    closes = len(_HTML_CLOSE_TAG_RE.findall(working))
    return opens - closes


def _python_open_block(line):
    stripped = line.strip()
    if stripped.startswith("#"):
        return False
    if stripped.endswith(":"):
        return True
    return False


def _python_starts_dedent(line):
    stripped = line.lstrip()
    return stripped.startswith(("elif ", "else:", "except", "finally:"))


def _python_is_docline(line):
    stripped = line.strip()
    return stripped.startswith(('"""', "''"))


def _markdown_list_indent(line):
    """Return markdown list depth hint from leading spaces and marker type."""
    match = re.match(r"^(\s*)([-*+]\s+|\d+\.\s+)", line.rstrip())
    if not match:
        return None

    spaces = len(match.group(1).replace("\t", "    "))
    return int(spaces / 2) + 1


def format_text(text, language, indent_unit):
    """Return smart-indented text using lightweight language heuristics."""
    lines = text.splitlines()
    if not lines:
        return text

    formatted = []
    depth = 0
    in_markdown_fence = False
    html_embedded_language = None

    for raw in lines:
        stripped = raw.strip()
        lowered = stripped.lower()

        if language == "markdown" and stripped.startswith("```"):
            formatted.append(stripped)
            in_markdown_fence = not in_markdown_fence
            depth = 0
            continue

        if not stripped:
            formatted.append("")
            if language == "markdown":
                depth = 0
            continue

        if language == "markdown" and in_markdown_fence:
            formatted.append(stripped)
            continue

        effective_depth = depth
        if _line_starts_with_closer(raw, language):
            effective_depth = clamp_depth(depth - 1)

        if language == "markdown":
            list_depth = _markdown_list_indent(raw)
            if list_depth is not None:
                effective_depth = clamp_depth(list_depth - 1)

        if language == "html" and html_embedded_language:
            if lowered.startswith(("</script", "</style")):
                effective_depth = clamp_depth(depth - 1)
            elif _line_starts_with_closer(raw, html_embedded_language):
                effective_depth = clamp_depth(depth - 1)

        if language == "python" and _python_is_docline(raw):
            # Keep docstring fence lines aligned with current scope.
            formatted.append((indent_unit * clamp_depth(effective_depth)) + stripped)
            depth = effective_depth
            continue

        formatted.append((indent_unit * clamp_depth(effective_depth)) + stripped)

        if language == "html" and html_embedded_language and not lowered.startswith(("</script", "</style")):
            delta = _brace_delta(raw)
            if _line_starts_with_closer(raw, html_embedded_language):
                depth = clamp_depth(effective_depth + max(delta, 0))
            else:
                depth = clamp_depth(effective_depth + delta)
            continue

        if language in ("html", "jsx", "tsx"):
            depth = clamp_depth(effective_depth + _html_delta(raw))

            if language == "html":
                if lowered.startswith("<script"):
                    html_embedded_language = "javascript"
                elif lowered.startswith("</script") and html_embedded_language == "javascript":
                    html_embedded_language = None
                elif lowered.startswith("<style"):
                    html_embedded_language = "css"
                elif lowered.startswith("</style") and html_embedded_language == "css":
                    html_embedded_language = None
        elif language == "python":
            if _python_open_block(raw):
                depth = effective_depth + 1
            elif _DEF_OR_CLASS_RE.match(stripped):
                depth = effective_depth + 1
            elif stripped.startswith(PYTHON_DEDENT_PREFIXES):
                depth = effective_depth
            else:
                depth = effective_depth
        elif language == "markdown":
            list_depth = _markdown_list_indent(raw)
            if list_depth is not None:
                depth = list_depth
            elif stripped.endswith(":"):
                depth = effective_depth + 1
            else:
                depth = 0
        else:
            delta = _brace_delta(raw)
            if _line_starts_with_closer(raw, language):
                depth = clamp_depth(effective_depth + max(delta, 0))
            else:
                depth = clamp_depth(effective_depth + delta)

    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(formatted) + suffix
