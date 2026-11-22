#!/bin/bash
# Sets the Terminal tab title to "<icon> <folder>" for the Claude session that ran the hook.
# Usage: tab-title.sh idle|working|attention
case "$1" in
  working)   icon="⏳" ;;
  attention) icon="🔔" ;;
  *)         icon="🟢" ;;
esac
name=$(basename "${CLAUDE_PROJECT_DIR:-$PWD}")
# Find the controlling terminal by walking up the process tree.
pid=$$
for _ in 1 2 3 4 5 6; do
  t=$(ps -o tty= -p "$pid" 2>/dev/null | tr -d ' ')
  if [ -n "$t" ] && [ "$t" != "??" ]; then
    printf '\033]0;%s %s\007' "$icon" "$name" > "/dev/$t" 2>/dev/null
    exit 0
  fi
  pid=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ')
  [ -z "$pid" ] || [ "$pid" = 1 ] && break
done
exit 0
