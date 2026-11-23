#!/bin/bash
# Link this repo's skills and hooks into Claude Code and Codex.
# Safe to re-run. Never overwrites a real file or folder; it reports it instead.
# Usage: ./install.sh [--dry-run]                      global skills and hooks
#        ./install.sh [--dry-run] --project DIR NAME   turn on project-skills/NAME in one project only
set -u
repo="$(cd "$(dirname "$0")" && pwd)"
dry=0; [ "${1:-}" = "--dry-run" ] && { dry=1; shift; }

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

if [ "${1:-}" = "--project" ]; then
  dir="${2:?project folder}"; name="${3:?skill name}"; src="$repo/project-skills/$name"
  [ -d "$src" ] || { echo "No project skill named $name in $repo/project-skills"; exit 1; }
  dir="$(cd "$dir" && pwd)"
  link "$src" "$dir/.claude/skills/$name"   # Claude Code
  link "$src" "$dir/.agents/skills/$name"   # Codex
  exit 0
fi

for skill in "$repo"/.agents/skills/*/; do
  name="$(basename "$skill")"
  link "${skill%/}" "$HOME/.claude/skills/$name"
  [ -d "$HOME/.codex" ] && link "${skill%/}" "$HOME/.codex/skills/$name"
done

for hook in "$repo"/claude/hooks/*; do
  link "$hook" "$HOME/.claude/hooks/$(basename "$hook")"
done

for style in "$repo"/claude/output-styles/*.md; do
  [ -e "$style" ] && link "$style" "$HOME/.claude/output-styles/$(basename "$style")"
done
