# How I work (every project)

- I type fast with typos. Read for intent; don't ask about spelling.
- If I need to act or decide, say that first. Ask one plain question at a time.
- When I say I don't know an answer, use logic or search the web and make the call.
- Discussing a design is not a go-ahead. Don't start building until I say so, and don't take on
  a big batch at once; use parallel subagents when work splits cleanly.
- Git: never push or merge to main without my approval. Work on a branch, one PR off the latest main.
- Restructuring or condensing docs: lose no information, examples or decisions. Prefer plain,
  standard Markdown and fewer files; challenge structure that adds complexity.
- Writing for me: linear and readable, with tables, bullets and headings where they help, but
  don't over-bold. Diagrams should explain, not compress.
- Artifacts I view on my phone (dashboards, workflow pages): follow
  `~/Developer/kk_productivity/design/artifact-layout.md` (shared tokens, phone layout, folding items).
  Long answers and design docs don't use it: Claude's default design, no phone rules; design docs
  are desktop layouts.
- When a single answer is long and needs focused reading (a report, research, a comparison) and the
  terminal is the wrong place to read it, put that one answer on a plain, readable HTML page and give a
  2-3 line summary in chat. Only for that answer: never a log or summary of the session, and not for
  normal replies. At the Mac, write `<repo>/.answers/index.html` (globally gitignored), replacing
  whatever was there, and `open` it; when I'm on my phone, use the repo's one artifact.
- Never change my notes or vault (Obsidian, Notion exports) without asking.
- I'm not an expert Claude Code user yet: when a built-in feature would help, name it and how to
  use it. Prefer built-ins over custom skills or layers; custom tools are plain scripts, MCP only
  when nothing simpler works.
- Code: do the simplest thing that works. Plain functions, few dependencies, cautious upgrades.
- Scripts that agents or scheduled runs call: fast, short output, clear error messages, never hang;
  log each run to a file the next session can read; refuse to start if already running.
- Notifications go to TickTick, never email.
