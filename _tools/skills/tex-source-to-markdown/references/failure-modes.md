# Failure Modes

Use this file when the baseline conversion looks plausible but is not faithful enough to hand off.

## What Worked Repeatedly

- Keep the original archive and extracted `<Paper>_source/` untouched.
- Identify the real entry TeX file before converting anything.
- Run baseline conversion from the source directory so relative `\input` paths resolve.
- Fall back to per-section conversion when whole-document conversion is unstable.
- Render PDF-only figures to large PNG files for Markdown Preview Enhanced.
- Add explicit `**Figure N.**`, `**Table N.**`, and `**Algorithm N.**` captions so textual references are locatable.
- Use the source TeX as the authority when cleaning tables, captions, or grouped figures.
- Preserve a minimal explicit anchor layer (`<a id="..."></a>`) when the document depends on many internal links.
- Normalize anchor ids and link targets before rewriting numeric links into prose like `Figure 9` or `Section 3.5`.
- Expand giant prompt appendix tables into per-item Markdown blocks when table cells contain many escaped `\n` lines.
- Scan rewritten Markdown for control characters when math-heavy lines were edited by script.
- Re-render fresh PNGs from the source PDFs when MPE shows figures as shifted or incomplete.

## What Failed Repeatedly

- Whole-document `pandoc` conversion can hang on expanded TeX or heavily split projects.
- Converters may silently drop prompt tables, grouped headers, or `multirow` content.
- Raw HTML tables and `<span>` wrappers often survive conversion and trigger Markdown Preview Enhanced parse issues.
- `audit_refs.py` can report a clean file while long HTML table blocks still remain, especially when numbering itself happens to be internally consistent.
- Math-wrapped labels such as `$\mbox{LLaMA}_{\mbox{\small 7B}}$` can be valid LaTeX but poor Markdown output.
- Inline PDF embeds are unreliable in Markdown Preview Enhanced even when the file path is correct.
- Auditing only unresolved labels is not enough; numbering can still drift even when the file "looks done".
- A document can read smoothly after prose cleanup while still be missing explicit figure or table captions needed for numbering alignment.
- Removing all HTML mechanically can break internal navigation if the remaining anchors were the only stable link targets.
- Leaving ids with spaces or inconsistent naming leads to fragile jumps in Markdown Preview Enhanced.
- Keeping appendix prompt data in a wide Markdown table often produces unreadable output even if the table is technically valid.
- `audit_refs.py` can report missing prose references when the file still uses numeric markdown links rather than explicit `Figure N` text.
- Removing placeholder captions or inserting recovered tables can shift later table numbers, leaving the body prose still pointing to the old numbering.
- Large block replacements can accidentally delete adjacent explanatory prose, which then surfaces later as "caption without ref" or as a table that exists but is no longer introduced in the text.
- Patching nested `<thead>` / `<tbody>` fragments one by one is brittle; it often leaves residual wrappers or duplicate heading/caption artifacts behind.
- Cleanup rewrites can accidentally degrade semantic symbols such as `†`, `✓`, and `×` into placeholder words like `dagger`, `check`, or `x`, which weakens fidelity even when the file still audits cleanly.
- A document can preserve all table numbers yet still be wrong if the Markdown table blocks were permuted relative to the source `\input{table/...}` order.
- A file can pass `audit_refs.py` and still throw ParseError in Markdown Preview Enhanced because scripted rewrites inserted control characters or damaged TeX escapes.
- High-risk math formatting such as `\textsc`, `\texttt`, or unusual TeX wrappers can parse poorly in Markdown math renderers even when the source TeX itself is valid.
- Blind whitespace cropping of existing PNGs can make figures appear shifted or incomplete by changing the effective page framing.
- A PNG may exist and resolve correctly in Markdown while still being the wrong asset because it was rendered from the PDF with unstable framing or later over-cropped.

## Preferred Recovery Path

1. Re-check the main TeX entry.
2. Retry conversion from the source directory instead of the workspace root.
3. If whole-document conversion is slow or broken, convert section files individually and concatenate them.
4. Replace PDF-only figure embeds with PNG/JPG assets and Markdown image syntax.
5. Rebuild complex tables into pure Markdown when HTML or TeX residue remains.
6. For a long damaged appendix block, rebuild the tables as bounded source-backed chunks rather than patching HTML tags individually.
7. After each chunk replacement, remove obsolete placeholder captions and immediately re-check prose references for renumbering drift.
8. If the source uses split table files, verify that Markdown table order still matches the `\input{table/...}` order in the TeX entry and supplementary files.
9. Preserve meaningful symbols such as `†`, `✓`, and `×` rather than rewriting them into placeholder words.
10. Stabilize internal anchors and link targets before removing the last structural HTML wrappers.
11. If preview parsing still fails, scan the Markdown for control characters and simplify fragile math notation before changing more structure.
12. If figures still look clipped, re-render fresh full-page PNGs from the source PDFs before attempting any manual crop.
13. Re-run `scripts/audit_refs.py` and manually inspect any reported mismatch instead of assuming the document is done because it reads cleanly.

## Table-Specific Recovery

Treat these as high-risk tables:

- prompt tables
- ablation tables with grouped labels
- tables using `multirow`, `multicolumn`, `cmidrule`, or `\includegraphics`
- tables that mix math, text sizing commands, and model names

For those tables:

1. Read the source TeX block directly.
2. Flatten grouped headers and row groups into a plain Markdown table.
3. Replace parse-hostile TeX snippets with readable text when the semantic content is unchanged.
4. Confirm the final row order and labels against the source.
5. If the table cluster spans multiple numbered tables, map the full number order before editing so later prose references do not drift silently.
6. Preserve source symbols with meaning in the table body or caption, especially `†`, `‡`, `✓`, and `×`.

## Math And Rewrite Recovery

Use this when the structure seems correct but preview still throws ParseError.

1. Inspect recently rewritten lines for hidden control characters such as backspace or tab.
2. Confirm TeX backslashes survived any Python or scripted rewrite literally.
3. Replace fragile renderer-specific math formatting with more conservative forms when the meaning is unchanged.
4. Reopen preview after the math cleanup instead of assuming a green audit means the parse issue is gone.

## Image Recovery

Use this when figures exist locally but appear shifted, clipped, or incomplete.

1. Treat the source PDF as the image authority.
2. Re-render a fresh full-page PNG from the PDF before editing the old PNG.
3. Compare the PNG framing against the source PDF page or crop box if the aspect ratio looks suspicious.
4. Only crop whitespace after you verify the full page render is correct.
5. Avoid blind non-white bbox cropping as a default recovery path.

## Large-Block Recovery

Use this when the remaining bad conversion output is concentrated in one long section such as dataset introductions, supplementary comparisons, or appendix prompt dumps.

1. Identify the whole damaged span in Markdown with stable boundary markers.
2. Map every table in that span from the source TeX before editing.
3. Replace the full span with reconstructed Markdown tables or per-item blocks, not piecemeal HTML cleanup.
4. Re-read the paragraphs immediately before and after the replaced span to ensure no explanatory prose was removed.
5. Compare the final Markdown table order against the source `\input{table/...}` order, not just the visible caption numbers.
6. Search the document for the affected table numbers and update any stale prose references.
7. Audit again only after the prose and numbering around that span are stable.

## Reference-Specific Recovery

If the Markdown still contains many internal links after table and figure cleanup:

1. List all explicit anchors and all `(#...)` link targets.
2. Normalize ids with spaces or unstable naming into slug-like ids.
3. Patch the links to the normalized ids.
4. Add explicit anchors for appendix sections or tables that are linked but do not yet have a target.
5. Remove duplicate anchors with the same id.
6. Only after the anchor map is stable, rewrite numeric links into readable prose where desired.
