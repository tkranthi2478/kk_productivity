#!/bin/bash
# Link this repo's skills and hooks into Claude Code and Codex.
# Safe to re-run. Never overwrites a real file or folder; it reports it instead.
# Usage: ./install.sh [--dry-run]
set -u
repo="$(cd "$(dirname "$0")" && pwd)"
dry=0; [ "${1:-}" = "--dry-run" ] && dry=1

link() {  # link <source> <target>
  src="$1"; dst="$2"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    echo "ok       $dst"; return
  fi
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    echo "SKIP     $dst exists and is not a link (move it, then re-run)"; return
  fi
  echo "link     $dst -> $src"
  [ $dry = 1 ] || { mkdir -p "$(dirname "$dst")"; ln -sfn "$src" "$dst"; }
}

for skill in "$repo"/.agents/skills/*/; do
  name="$(basename "$skill")"
  link "${skill%/}" "$HOME/.claude/skills/$name"
  [ -d "$HOME/.codex" ] && link "${skill%/}" "$HOME/.codex/skills/$name"
done

for hook in "$repo"/claude/hooks/*; do
  link "$hook" "$HOME/.claude/hooks/$(basename "$hook")"
done
