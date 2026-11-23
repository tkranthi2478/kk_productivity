# kk_productivity

This repo is the source of truth for the owner's Claude Code / Codex setup.
Files here are symlinked into `~/.claude` and `~/.codex` by `./install.sh`, so
edits are live immediately.

- New skill: `.agents/skills/<name>/SKILL.md` (+ `scripts/`), add a line to the
  README, then run `./install.sh`.
- New hook script: `claude/hooks/`, then `./install.sh`. Wiring it into
  `~/.claude/settings.json` is a separate step the owner approves.
- Never commit secrets, tokens, emails or `settings.json`.
- Global skills (`.agents/skills/`) load in every session, so keep only ones used across
  projects there. Skills for one kind of job go in `project-skills/` and are turned on per
  project with `./install.sh --project DIR NAME`. Skills tied to one repo's code (e.g. `hi`)
  live in that repo.
