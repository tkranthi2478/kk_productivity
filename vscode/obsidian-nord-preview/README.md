# Obsidian Nord Markdown Colors

Local VS Code extension applying only heading, bold, and italic colors to the built-in Markdown preview in every folder.

Headings H1–H6: `#bf616a`, `#ebcb8b`, `#a3be8c`, `#b48ead`, `#8fbcbb`, `#81a1c1`.
Bold and italic: `#ebcb8b` in dark mode, `#a3be8c` in light mode.
Colors copied from the installed Obsidian Nord theme. No executable extension code or dependencies.

## Install

Run `python3 build.py`, then `code --install-extension obsidian-nord-preview-1.0.0.vsix --force`.
Reload VS Code with **Developer: Reload Window** after first installation.
Disable **Obsidian Nord Markdown Colors** to turn the colors off.

Uses `markdown.previewStyles`, which lets VS Code load the stylesheet from the extension. An absolute path in `markdown.styles` outside a workspace can be blocked by preview resource restrictions. Existing workspace CSS can override these colors.
