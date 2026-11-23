# Compact reading profile

This is the profile established while reformatting *Mastering Behavioral
Interviews* in November 2026. It is an example to reuse when requested, not a
mandatory design for other books.

| Property | Accepted setting or behavior |
| --- | --- |
| Page | US Letter, portrait |
| Margins | 0.65 inches on all sides |
| Font family | Minion Pro, using the user's available fonts |
| Ordinary body text | 11.5 pt, reduced from the approved 12 pt rendering |
| Ordinary headings | 0.5 pt below their original effective size |
| Nested nonitalic content | Original size retained, usually 12 pt |
| Italic content | Subsequently reduced by 0.5 pt, usually 12 to 11.5 pt |
| Ordinary paragraph gaps | Explicit 4 pt after, zero before |
| Heading gaps | Approximately 5 pt before, 3 pt after, adjusted to hierarchy |
| Leading | Existing 14.4 pt minimum for ordinary text; review mixed-size lines |
| Citations | Inline, raised superscript, with original links preserved |
| Renderer | LibreOffice; Pages was rejected because of import/rendering problems |
| Pagination | Widows/orphans controlled; short paragraphs, labels, captions, and small tables grouped |

## Lessons from the reference conversion

- The approved original PDF used Letter pages and 12 pt body text, despite
  earlier conversion commands mentioning a 7-inch book trim and 7 pt type.
  Measuring the actual artifact prevented applying the wrong baseline.
- There were 130 paragraphs containing only reference markers. Inlining those
  markers required an additional superscript formatting step.
- Nine source tables had conversion defects. The Story Catalog contained six
  meaningful columns separated by five empty spacer columns; a plausible-looking
  PDF initially displayed only Story and its two row labels.
- A six-column table was made readable with widths totaling the text area and
  content-based proportions. The final balance was approximately 15/13/20/16/18/18
  percent across Story, Context, Actions, Results, Learnings, and Signal Areas,
  with narrow spacer columns handled separately. Recompute for different content.
- An acknowledgments table hid one column of names. Replacing that layout table
  with a compact paragraph list restored all 33 names.
- Validation ultimately compared all 66 nonempty narrative-table cells against
  cell-aware PDF extraction. These are reference-specific counts, not invariants
  for future books.

Do not bundle the book, the user's font files, or the generated PDFs with this
skill. Use the user's chosen source artifacts when applying the workflow.
