# Normalization Checklist

Use this checklist after the first TeX-to-Markdown conversion pass.

## Required Checks

- Source bundle extracted into `<Paper>_source/`
- Main TeX entry identified correctly
- Main Markdown file written next to the archive
- Image assets stored locally and linked with relative paths
- Markdown Preview Enhanced can render the images
- If direct whole-document conversion failed, the fallback path is documented and the current Markdown came from the reliable path, not a half-broken attempt

## Conversion Path Checks

- Run conversion from the source directory when the project uses relative `\input` or `\include`
- Ignore commented include lines when expanding TeX inputs
- If whole-document conversion hangs or produces badly broken structure, switch to per-file conversion instead of forcing the full document path

## Reference Integrity

Search for unresolved labels:

```bash
rg -n '\\[(fig|tab|alg|sec|subsec|eq):[^]]+\\]' /path/to/paper.md
```

Search for caption residue and TeX-ish prose residue:

```bash
rg -n '^\\*Caption:|Figure\\.|Table\\.|Algorithm\\.' /path/to/paper.md
```

Search for HTML table and wrapper residue:

```bash
rg -n '<table\\b|<div class="table\\*">|<span\\b|<figure\\b|<embed\\b' /path/to/paper.md
```

Search for lingering low-level HTML table fragments that can survive even when higher-level wrappers are gone:

```bash
rg -n '<thead>|<tbody>|<tr>|<td\\b|<th\\b' /path/to/paper.md
```

Search for duplicated reference prefixes:

```bash
rg -n '\\b(Figure|Table|Section|Appendix)\\s+\\1\\b' /path/to/paper.md
```

Search for placeholder caption stubs that often remain after manual cleanup:

```bash
rg -n '^\\*\\*(Figure|Table|Algorithm) [0-9]+\\.\\*\\*$' /path/to/paper.md
```

If the document still contains internal markdown links, verify that every target exists:

```bash
python3 - <<'PY'
from pathlib import Path
import re
text = Path('/path/to/paper.md').read_text()
anchors = set(re.findall(r'<a id="([^"]+)"></a>', text))
links = sorted(set(re.findall(r'\]\(#([^)]+)\)', text)))
missing = [link for link in links if link not in anchors]
print('missing_count', len(missing))
for item in missing:
    print(item)
PY
```

Check for duplicate anchors:

```bash
python3 - <<'PY'
from pathlib import Path
import re
from collections import Counter
text = Path('/path/to/paper.md').read_text()
ids = re.findall(r'<a id="([^"]+)"></a>', text)
for key, value in Counter(ids).items():
    if value > 1:
        print(value, key)
PY
```

Run the audit script:

```bash
python3 scripts/audit_refs.py /path/to/paper.md
```

If the file was heavily rewritten by script, check for hidden control characters that can trigger preview parse failures:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('/path/to/paper.md').read_text()
for i, line in enumerate(text.splitlines(), 1):
    bad = [hex(ord(ch)) for ch in line if ord(ch) < 32 and ch not in '\n\r']
    if bad:
        print(i, bad, repr(line))
PY
```

You should resolve:

- prose references with no matching caption number
- caption numbers that do not appear in the text when they should
- caption gaps that remain even though the surrounding prose already reads naturally
- unresolved label placeholders
- raw HTML figure wrappers
- raw HTML table wrappers and spans
- duplicated prose prefixes
- missing internal link targets
- duplicate anchors

If you rebuilt a large table range or appendix block, also verify:

- nearby explanatory prose was not accidentally deleted
- placeholder captions for the rebuilt tables are gone
- prose references after the edited block still point to the correct renumbered tables
- Markdown table order still matches the source `\input{table/...}` order when the paper uses split table files
- Markdown Preview Enhanced does not still show ParseError after the text cleanup

## Image Rules

- Use `![alt](relative/path.png)` or `![alt](relative/path.jpg)`
- Do not expect inline PDF embedding to work in MPE
- If a source figure is a PDF, render a sufficiently large PNG for display
- Keep the original source figure path available nearby if provenance matters
- If an image appears shifted or incomplete, re-render the PNG from the source PDF before attempting whitespace crops
- Compare suspicious PNG aspect ratios or framing against the source PDF page or crop box
- Avoid blind bbox-based whitespace cropping unless you verified the fresh full-page PNG already matches the source correctly

## Caption Rules

- Use `**Figure N.** ...` for figures
- Use `**Table N.** ...` for tables
- Use `**Algorithm N.** ...` for algorithms
- Put the caption immediately adjacent to the related image/table/block
- For multi-panel or grouped figures, keep a single explicit number for the group unless the source paper uses separate numbered figures

## Math And Block Cleanup

- Convert obvious display equations to `$$ ... $$`
- Reformat theorem-like blocks into readable Markdown
- Reformat algorithms into ordered steps or fenced blocks if raw conversion is unreadable
- Preserve numbering when the paper references the block elsewhere
- If preview still throws ParseError, simplify fragile math notation into conservative renderer-friendly forms when the semantics are unchanged
- After scripted rewrites, confirm TeX backslashes survived literally and were not consumed as escape sequences

## Table Cleanup

- Prefer pure Markdown tables when the user expects stable Markdown Preview Enhanced rendering
- Rebuild grouped headers or grouped row labels when conversion output is ambiguous
- Replace parse-breaking TeX such as nested `\mbox` fragments with readable text when the meaning is unchanged
- Validate row order, grouped labels, and caption numbering against the source TeX
- If appendix prompt tables are wide and cell content contains many escaped `\n` lines, prefer per-item blocks with headings and fenced code samples over a single giant table
- If one long HTML block covers many tables, map the full table order from the source before editing so later references can be rechecked systematically
- After replacing a multi-table block, search the body prose for the affected table numbers and fix stale references immediately
- Preserve meaningful source symbols such as `†`, `‡`, `✓`, and `×` instead of rewriting them into placeholder words

## Anchor And Link Rules

- It is acceptable to keep `<a id="..."></a>` as the only intentional HTML residue
- Normalize ids with spaces or ad hoc naming into stable slug-like ids
- Patch internal links after id normalization
- Add explicit anchors for appendix sections, tables, or figures when prose links point to them but no anchor exists
- Remove duplicate anchors with the same id
- If the document still uses numeric markdown links such as `[7](#fig:...)`, stabilize the anchor map before rewriting those references into prose

## Markdown Preview Enhanced Notes

- Relative paths are safer than absolute paths for shared Markdown files
- Cached previews can hide fixes; reopen preview after major cleanup
- Directories with spaces can be flaky in some setups; if needed, move generated assets to a no-space directory and update links consistently
- A green audit is not enough; explicitly check that preview has no remaining ParseError and that images are fully visible
