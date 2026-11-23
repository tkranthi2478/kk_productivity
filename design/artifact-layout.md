# Artifact layout (phone artifacts)

Artifacts I open on my phone (dashboards, trackers, workflow pages) use this so they look and
behave the same. Not for long answers (`.answers/`) or design docs: those use Claude's default design. Reference implementation: AI Skill Newsletter
(`~/Developer/kk_ai_skilling/newsletter/page.html`).

## Rules
- One column, `max-width: 720px`, side gutter `max(16px, env(safe-area-inset-*))`. Full width of
  that column, never a narrow strip.
- Order: title, 1-4 status lines (what needs me first), then section cards.
- Sections are fixed headings (not collapsible) with a status pill on the right.
- Items with detail fold to one line (caret, title, status pill); short items stay as plain
  bullets or table rows. Expand all / Collapse all when there are many folds.
- Tables: on phones (<= 560px) each row becomes a stacked card; never force sideways scrolling.
- Tap targets >= 44px. Several views on one page: tabs, with a `#hash` per view.
- Numbers only as evidence for a point. Hide dropped or reference-only items.
- Light and dark themes from the same tokens.

## Tokens
```css
:root {
  --bg: #eef1f4; --surface: #ffffff; --sunk: #e4e8ee; --ink: #16202b; --muted: #5a6676; --line: #d5dbe3;
  --accent: #0f6b74; --accent-soft: #dcefef;
  --good: #237a46; --good-soft: #def1e5; --warn: #9a5d06; --warn-soft: #f7ead3; --bad: #b02a22; --bad-soft: #f8e2df;
  --display: "Familjen Grotesk", "Inter", system-ui, sans-serif;
  --body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
/* dark (in both the prefers-color-scheme block and [data-theme="dark"]) */
  --bg: #0f141a; --surface: #171e26; --sunk: #121820; --ink: #e4e9ef; --muted: #96a2b2; --line: #28323e;
  --accent: #5cc4cc; --accent-soft: #15302f;
  --good: #74cf96; --good-soft: #15301f; --warn: #e9b25e; --warn-soft: #33270f; --bad: #f08a80; --bad-soft: #391915;
```
Fonts: Google Fonts `Familjen Grotesk` 500-700, `Inter` 400-600, `JetBrains Mono` 400-500.
Body 15px/1.55; h1 2rem (1.7rem on phones); section titles 1.15rem display 600.

## Components
```css
section.sec { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }
.sec-head { display: flex; gap: 10px; align-items: center; justify-content: space-between; padding: 14px 16px 6px; }
.sec-body { padding: 0 16px 16px; display: grid; gap: 4px; min-width: 0; }
.status { font: 500 .72rem/1 var(--mono); padding: 5px 8px; border-radius: 999px; background: var(--sunk); color: var(--muted); }
.status.good { background: var(--good-soft); color: var(--good); }   /* .warn, .bad the same way */
details.task { border-top: 1px solid var(--line); }
details.task > summary { list-style: none; cursor: pointer; display: grid; grid-template-columns: auto 1fr auto;
  gap: 10px; align-items: center; padding: 12px 0; min-height: 48px; }
.caret { width: 9px; height: 9px; border-right: 2px solid var(--muted); border-bottom: 2px solid var(--muted);
  transform: rotate(-45deg); }  details[open] > summary .caret { transform: rotate(45deg); }
details.task > .task-body { display: grid; gap: 8px; padding: 0 0 14px 20px; }
.next::before { content: "Next"; font: 500 .68rem/1.9 var(--mono); text-transform: uppercase; color: var(--accent); }
```
