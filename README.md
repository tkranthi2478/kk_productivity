# kk_productivity

My general productivity setup for Claude Code and Codex: skills, hooks and editor
tweaks, kept in one repo. `./install.sh` links them into `~/.claude` and `~/.codex`,
so editing a file here changes the live setup.

## Install

```bash
./install.sh --dry-run   # show what would be linked
./install.sh             # link skills and hooks; never overwrites real files
```

Re-run after adding a skill or hook.

## Layout

```
.agents/skills/<name>/   skills (SKILL.md + scripts/references), linked into
                         ~/.claude/skills and ~/.codex/skills
claude/hooks/            Claude Code hook scripts, linked into ~/.claude/hooks
                         (wired up in ~/.claude/settings.json)
vscode/                  VS Code extensions and tweaks
install.sh               the linker
```

## Skills

- [Format Ebook PDF](.agents/skills/format-ebook-pdf/SKILL.md): repair ebook
  typography, margins, paragraph spacing, table visibility, citation formatting,
  and pagination; verify the rendered PDF against its structured source.
- [YouTube Transcript](.agents/skills/yt-transcript/SKILL.md): download only a
  video's captions and write a clean, timestamped transcript with chapters.

## Hooks

- [tab-title.sh](claude/hooks/tab-title.sh): Terminal tab shows 🟢 idle, ⏳ working,
  🔔 needs attention for each Claude session.

## Editor

- [Obsidian Nord Markdown Colors](vscode/obsidian-nord-preview/README.md): VS Code
  preview heading, bold, and italic colors in every folder.

## Not here

- `hi` (Hello Interview capture) lives in `~/Developer/hi-tools` with its own skill.
- `~/.claude/settings.json` is not tracked: it holds machine-specific and private values.
