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

## What Failed Repeatedly

- Whole-document `pandoc` conversion can hang on expanded TeX or heavily split projects.
- Converters may silently drop prompt tables, grouped headers, or `multirow` content.
- Raw HTML tables and `<span>` wrappers often survive conversion and trigger Markdown Preview Enhanced parse issues.
- Math-wrapped labels such as `$\mbox{LLaMA}_{\mbox{\small 7B}}$` can be valid LaTeX but poor Markdown output.
- Inline PDF embeds are unreliable in Markdown Preview Enhanced even when the file path is correct.
- Auditing only unresolved labels is not enough; numbering can still drift even when the file "looks done".
- A document can read smoothly after prose cleanup while still be missing explicit figure or table captions needed for numbering alignment.
- Removing all HTML mechanically can break internal navigation if the remaining anchors were the only stable link targets.
- Leaving ids with spaces or inconsistent naming leads to fragile jumps in Markdown Preview Enhanced.
- Keeping appendix prompt data in a wide Markdown table often produces unreadable output even if the table is technically valid.
- `audit_refs.py` can report missing prose references when the file still uses numeric markdown links rather than explicit `Figure N` text.

## Preferred Recovery Path

1. Re-check the main TeX entry.
2. Retry conversion from the source directory instead of the workspace root.
3. If whole-document conversion is slow or broken, convert section files individually and concatenate them.
4. Replace PDF-only figure embeds with PNG/JPG assets and Markdown image syntax.
5. Rebuild complex tables into pure Markdown when HTML or TeX residue remains.
6. Stabilize internal anchors and link targets before removing the last structural HTML wrappers.
7. Re-run `scripts/audit_refs.py` and manually inspect any reported mismatch instead of assuming the document is done because it reads cleanly.

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

## Reference-Specific Recovery

If the Markdown still contains many internal links after table and figure cleanup:

1. List all explicit anchors and all `(#...)` link targets.
2. Normalize ids with spaces or unstable naming into slug-like ids.
3. Patch the links to the normalized ids.
4. Add explicit anchors for appendix sections or tables that are linked but do not yet have a target.
5. Remove duplicate anchors with the same id.
6. Only after the anchor map is stable, rewrite numeric links into readable prose where desired.
