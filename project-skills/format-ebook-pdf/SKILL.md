---
name: format-ebook-pdf
description: Reformat an ebook or converted DOCX into a readable PDF with controlled typography, margins, paragraph spacing, complete tables, superscript citation links, and sensible pagination. Use when improving book layout or repairing conversion defects while preserving the source content.
---

# Format an ebook PDF

Produce a PDF whose content and layout have both been verified. Prefer editing
the structured EPUB/DOCX source and re-rendering instead of modifying PDF glyphs.
Apply requested changes cumulatively to the latest verified source.

## Choose the source and renderer

- Identify the approved PDF and the editable document that actually produced it.
  Measure the PDF's page size, text bounds, and rendered font sizes. Filenames and
  conversion flags alone are not reliable evidence of the current layout.
- Preserve the original and write a clearly named revision. Keep the final DOCX
  as the editable source for subsequent changes.
- Use an existing DOCX when available. For EPUB input, Calibre's `ebook-convert`
  can supply a DOCX; inspect its output before trusting its formatting.
- Prefer LibreOffice for a scriptable DOCX-to-PDF workflow when the user has no
  different renderer preference. Use the bundled document runtime and
  `render_docx.py` when available. Follow the available document/PDF skills for
  rendering, artifact markers, and dependencies; do not pin a runtime version.
- Use Pages only when requested or accepted and its import is visually correct.
  If it misrenders the DOCX, repair the source or use another renderer. Do not
  deliver an earlier QA PDF after making further source changes.
- Verify actual PDF font families and font programs. Do not infer embedded
  fonts from a Calibre option, an installed font, a serif appearance, or a past
  converter's behavior. Subsetting is compatible with embedding.

## Inspect before editing

Run `scripts/inspect_conversion.py SOURCE.docx` to inventory table contents,
zero-width tables, standalone reference markers, and superscript links.
For a PDF candidate, add `--pdf CANDIDATE.pdf` to compare source table cells with
the rendered text. This optional check needs `pdfplumber` in the selected runtime.

Resolve effective formatting through document defaults, paragraph styles,
`basedOn`, character styles, and direct run properties. Account for OOXML style
toggle semantics when resolving bold and italic. Preserve fonts, images,
bookmarks, hyperlinks, numbering, and text unless the requested edit requires
a change.

## Typography, spacing, and margins

- Treat the approved reference and current request as the design authority.
  Use the [reference profile](references/reading-profile.md) only as a starting
  point when the user wants this reading style; its numbers are not universal.
- For selective font changes, compute the original effective size for each run.
  Apply a small explicit delta, usually 0.5 pt when the user asks for a slight
  reduction. Set both `w:sz` and `w:szCs` where appropriate.
- If nested content or italics must retain their size, protect them using
  effective formatting, numbering levels, indentation, and table context.
  A later request to shrink italics overrides the earlier italic exception.
- Verify rendered sizes, not just style definitions. Changing Normal does not
  override explicit sizes in other styles or runs.
- Use explicit paragraph `before`/`after` values in twips for predictable gaps.
  Remove conflicting line-unit `beforeLines`/`afterLines` overrides in the
  affected styles and paragraphs. Distinguish paragraph gaps from line leading.
- Do not change margins, page size, line leading, and font size together unless
  needed. State the chosen values so the revision is reviewable.

## Reference markers

- EPUB conversion can turn a citation such as `[3]` into its own paragraph.
  Merge a marker-only paragraph into the preceding paragraph in the same
  container. Do not delete it, attach it across a table boundary, or merge the
  actual endnote description into body prose.
- Move the complete hyperlink/bookmark nodes, not just visible text. Preserve
  anchor IDs, relationship IDs, destinations, and return links.
- Format inline numeric citation markers and short cross-reference markers as
  raised superscripts (`w:vertAlign="superscript"`), with a reduced apparent
  size. Do not raise ordinary linked titles, full URLs, or endnote labels.
- Inspect an exported example for both smaller glyphs and a raised baseline.
  In the PDF, check internal `/Dest` or `/GoTo` links as well as external URI
  links; some PDF libraries' `hyperlinks` lists include only external links.

## Tables and otherwise hidden content

- Converted tables may contain zero or automatic widths, empty spacer columns,
  absent `tblGrid`, oversized white cell borders, or malformed row properties.
  A PDF can look clean while showing only the first column.
- Inventory every source row and cell before editing. Set a real table width,
  `tblGrid`, and cell widths that sum to the available page width. Use fixed
  layout where automatic layout is unreliable.
- Assign widths according to content. Give long words room to wrap naturally;
  do not accept broken words such as `Communicat` / `ion` as a finished table.
  Keep intentional arrow columns narrow. Remove empty spacer columns only if
  their bookmarks and other non-text nodes are preserved.
- Remove obsolete cell borders that consume space. Use consistent light borders
  and modest padding. Allow rows to expand; avoid fixed heights that clip text.
- Repeat header rows, prevent an individual row from splitting when it fits,
  and keep short tables together when feasible. Keep captions with the table.
  Keep `trPr` before cells and maintain valid OOXML child ordering.
- A table used solely to position a list of names may be better represented as
  ordinary paragraphs. Preserve every name and bookmark. Inspect empty tables
  for images, fields, and anchors before removing them.

## Page endings

- Enable widow/orphan control on body paragraphs.
- Keep headings, short bold labels, and captions with the following content.
  Skip hyperlink-only TOC entries when inferring headings, or the entire TOC
  may become one chained block.
- Keep short paragraphs and individual list items intact when reasonable;
  allow long paragraphs to flow. Do not apply `keepNext` to all body text.
- Keep short reference descriptions with their following URL. Keep images with
  their captions where both fit without a large blank area.
- Preserve deliberate chapter/part openings unless the user asks for continuous
  flow. Use manual page breaks only for specific remaining defects after a
  complete render, not as the first pagination strategy.

## Verification and delivery

1. Compare source and edited text, link targets, bookmarks, images, and table
   cells. Any intentional representation change must preserve the content.
2. Render the latest DOCX and inspect page images. Contact sheets help find
   suspect pages but do not prove small text and tables are readable. Inspect
   every table and affected page boundary at readable resolution.
3. Run the inspector with `--pdf`. PDF text extraction interleaves table columns;
   compare cell text using cell geometry. An unverified cell is a reason to
   inspect, not proof that it is missing. Count and check all source cells.
4. Check the final PDF's margins, paragraph gaps, actual fonts, superscripts,
   internal and external links, tables, image captions, and paragraph endings.
   XML correctness alone does not establish rendering correctness.
5. Deliver the latest verified PDF with its page count. Provide the corresponding
   DOCX when requested; keep QA images and intermediate PDFs out of the handoff.
   Do not claim completeness from a page count, a clean cover, or a few sampled
   body pages.
