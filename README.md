# Smart Indent (Sublime Text 3)
![Sublime Text](https://img.shields.io/badge/Sublime%20Text-Plugin-orange)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success)
![Code Style](https://img.shields.io/badge/code%20style-consistent-brightgreen)

Smart Indent is a Sublime Text 3 plugin that formats a file using lightweight, rules-based indentation.
It detects language from both file extension and syntax, then applies language-specific indentation patterns.

## Features

- Command Palette command: **Smart Indent: Format File**
- Optional auto-format on save (`format_on_save` setting)
- Respects editor indentation preferences:
  - `translate_tabs_to_spaces`
  - `tab_size`
- Rules-based indentation engine (not just whitespace normalization)
- Handles common edge cases (HTML void tags, markdown code fences, comment/string-safe brace counting)
- Safe plain-text fallback for unsupported content

## Supported Languages

- HTML
- CSS
- JavaScript
- TypeScript
- TSX
- JSX
- JSON
- Python
- Markdown (basic)
- Plain text fallback

## Installation

### Manual Installation

1. In Sublime Text, open **Preferences → Browse Packages...**
2. Create a folder named `SmartIndent`
3. Copy this repository's files into that folder
4. Restart Sublime Text

### Package Control (if published)

1. Open Command Palette
2. Run `Package Control: Install Package`
3. Search for `Smart Indent`

> If the package is not published yet, use manual installation.

## Usage

### Format a file manually

- Open Command Palette and run **Smart Indent: Format File**
- Or use keybinding:
  - Windows/Linux: `Ctrl+Alt+I`
  - macOS: `Super+Alt+I`

### Enable format-on-save

Add to `SmartIndent.sublime-settings`:

```json
{
  "format_on_save": true
}
```

## How It Works

1. Detect language using file extension first
2. If extension is unknown, infer from `view.settings().get("syntax")`
3. Apply indentation rules:
   - HTML: opening/closing tag depth
   - JS/TS/TSX/JSX/JSON/CSS: bracket and brace delta
   - Python: `:` block open + known dedent starters
   - Markdown: basic list/numbered-list nesting + fenced code block passthrough
   - Text: no-op fallback

## Before / After Examples

### JavaScript

Before:

```js
function demo(){
if (ready){
console.log("ok")
}
}
```

After:

```js
function demo(){
    if (ready){
        console.log("ok")
    }
}
```

### Python

Before:

```py
def run():
if True:
return 1
```

After:

```py
def run():
    if True:
        return 1
```

## Repository Structure

- `smart_indent_plugin.py` — Sublime commands and save hook
- `smart_indent_languages.py` — language detection
- `smart_indent_engine.py` — formatting logic
- `smart_indent_utils.py` — indent utility helpers
- `SmartIndent.sublime-settings` — package settings
- `Default.sublime-commands` — command palette integration
- `Main.sublime-menu` — menu integration
- `Default (*.sublime-keymap)` — keyboard shortcuts
- `tests/test_engine.py` — unit tests for detection and formatting

## Limitations

- Formatter is intentionally heuristic and not an AST formatter
- Markdown support remains lightweight (not a full markdown parser)
- Complex embedded-language cases (e.g., script blocks in HTML) are best-effort

## Future Improvements

- Add richer language rules for YAML, XML, and SQL
- Add per-language toggles/settings
- Improve multiline string/comment awareness
- Add benchmarks and larger regression test fixtures
