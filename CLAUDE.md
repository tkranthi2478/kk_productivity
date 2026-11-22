# kk_productivity

This repo is the source of truth for the owner's Claude Code / Codex setup.
Files here are symlinked into `~/.claude` and `~/.codex` by `./install.sh`, so
edits are live immediately.

- New skill: `.agents/skills/<name>/SKILL.md` (+ `scripts/`), add a line to the
  README, then run `./install.sh`.
- New hook script: `claude/hooks/`, then `./install.sh`. Wiring it into
  `~/.claude/settings.json` is a separate step the owner approves.
- Never commit secrets, tokens, emails or `settings.json`.
- Skills must stay general. Project-specific skills (e.g. `hi`) live in their own repo.
