---
name: tex-source-to-markdown
description: Convert academic paper TeX source archives into high-fidelity Markdown that stays aligned with the original TeX/compiled paper. Use this skill when the user provides an arXiv/source tarball, zip, or extracted TeX project and wants a local Markdown version with preserved section structure, formulas, figures, tables, captions, algorithm numbering, and Markdown Preview Enhanced-compatible image paths. Also use it when fixing broken conversion artifacts such as unresolved labels like [alg:training], Figure. 7 style residue, missing Figure/Table numbers, or images that do not render in Markdown.
---

# TeX Source To Markdown

## Purpose

Turn a paper's TeX source bundle into a local Markdown file that is usable for reading and note-taking without losing the structure that matters: section numbering, display math, figures, tables, captions, algorithms, and cross-references.

The default target is not "best effort plain text". The target is a Markdown artifact that remains traceable to the TeX source and renders correctly in Markdown Preview Enhanced.

## When To Use This Skill

- The user gives a `.tar.gz`, `.zip`, or extracted TeX project for a paper
- The user wants a paper converted from TeX source to Markdown
- The user says the current Markdown does not match the TeX / compiled output
- Figures, tables, algorithms, or section references lost their numbering
- Markdown renders but images do not show in Markdown Preview Enhanced
- Conversion left HTML residue, unresolved labels, broken math blocks, or bad captions

## Output Layout

Prefer keeping all outputs next to the original archive:

```text
<Paper>.tar.gz
<Paper>_source/
<Paper>.md
<Paper>_md_images/
```

Rules:

- Keep the extracted source tree as the fidelity-preserving archive
- Write one main Markdown file per paper
- Put rendered image assets in `<Paper>_md_images/`
- Use relative paths from the Markdown file to image assets
- Treat the extracted source tree as the recovery point when the Markdown needs recalibration

## Workflow

### 1. Extract The Source Bundle Without Modifying It

Unpack the archive into `<paper-stem>_source/` and keep the original files intact. Do not treat the Markdown output as the canonical archive; the extracted TeX project is the canonical source.

If the user already provided an extracted directory, work in place and avoid rewriting source files unless the task explicitly requires it.

### 2. Find The Real Main TeX Entry

Do not assume `main.tex`.

Check likely entry files such as:

- `main.tex`
- `ms.tex`
- `paper.tex`
- `sample-sigconf.tex`

Use simple heuristics:

- Prefer files containing `\\documentclass`
- Prefer files containing `\\begin{document}`
- Inspect whether the file is a thin wrapper around `\\input` / `\\include`

If the project is split across multiple files, ensure the chosen entry file actually represents the full paper before conversion.

If you need to build an expanded TeX file from `\input` or `\include`, ignore commented include lines. Do not accidentally pull disabled appendix fragments or draft snippets into the Markdown.

### 3. Produce A Baseline Markdown Conversion

Use the source project to generate the first-pass Markdown. A direct converter such as `pandoc` is acceptable for the baseline, but treat the result as a draft that will need cleanup.

Baseline goals:

- preserve section headings
- preserve display math when possible
- extract media into a local directory
- keep the Markdown readable enough for post-processing

Do not stop after the first conversion pass.

Prefer this escalation order:

1. Try a direct conversion from the real source directory so relative `\input` paths resolve.
2. If whole-document conversion fails, hangs, or produces obviously broken structure, switch to per-file conversion and concatenate the sections in source order.
3. If a section is still unstable, use the source TeX and the compiled artifact as ground truth and rewrite that block manually.

Do not keep retrying a stuck whole-document conversion when per-section conversion is clearly more reliable.

### 4. Normalize Images For Markdown Preview Enhanced

Markdown Preview Enhanced is much more reliable with image formats such as PNG/JPG than with inline PDF objects.

Rules:

- Prefer standard Markdown image syntax: `![alt](relative/path.png)`
- Do not rely on `![](...pdf)` for inline rendering
- Replace HTML remnants such as `<figure>`, `<embed>`, or custom blocks with plain Markdown
- If a figure asset is only available as PDF, render it to a sufficiently large PNG and store it under `<Paper>_md_images/`
- Keep the original source asset path visible near the figure when traceability matters

On macOS, `qlmanage` is usually a pragmatic PDF-to-PNG fallback for Markdown Preview Enhanced. In sandboxed environments it may require escalation because it invokes Quick Look outside the workspace.

For MPE compatibility:

- prefer relative paths, not absolute paths
- avoid broken HTML wrappers
- if directory names contain spaces and rendering is flaky, either URL-encode them or rename the generated asset directory to a no-space variant and update links consistently

### 5. Restore Figure, Table, Algorithm, And Section Numbering

This is the critical calibration step.

The Markdown must not leave references in forms such as:

- `[alg:training]`
- `[tab:method]`
- `Figure. 7`
- bare images with no explicit figure number

Normalization rules:

- every image-backed figure referenced in the text should have an explicit caption line like `**Figure 7.** ...`
- every table referenced in the text should have an explicit caption line like `**Table 3.** ...`
- algorithms should appear as explicit numbered blocks, for example `**Algorithm 1.** ...`
- normalize prose references to `Figure 7`, `Table 3`, `Algorithm 1`, `Section 4.2`
- if the Markdown already contains internal links such as `[7](#fig:...)`, stabilize the target anchors first, then optionally rewrite the prose to `Figure 7`, `Table 3`, `Section 4.2`, or `Appendix 12.3`

Recover numbers from the source project, not by guessing. Use the TeX structure, nearby captions, and compiled numbering artifacts when available.

Combination figures are allowed: one `Figure N` may correspond to multiple images. In that case, keep the images grouped and attach one explicit `Figure N.` caption for the group.

### 5a. Stabilize Internal Anchors Before Final Prose Cleanup

Many converted papers remain navigable only because of HTML anchors such as `<a id="..."></a>`.

Rules:

- keep a thin explicit anchor layer when the Markdown uses many internal links
- it is acceptable to preserve `<a id="..."></a>` even after other HTML residue is removed
- normalize unstable ids that contain spaces or mixed ad hoc naming into stable slug-like ids
- ensure every `(#...)` link target has a matching explicit anchor
- remove duplicate anchors with the same id

Suggested order:

1. normalize target ids
2. patch links to the normalized ids
3. add missing anchors for appendix sections, subsections, or tables that are referenced but have no explicit target
4. only then rewrite numeric links into more readable prose such as `Figure 9`

Do not remove the final anchor layer if doing so would force Markdown Preview Enhanced to guess heading slugs.

### 6. Clean Math And Structured Blocks

Common conversion artifacts:

- broken display math spread across prose lines
- theorem/definition/proposition environments flattened into plain paragraphs
- algorithm bodies losing indentation

Fix these into Markdown-friendly forms:

- display math as `$$ ... $$`
- readable ordered or fenced blocks for algorithms
- explicit theorem/proposition labels when numbering matters

The goal is not typographic perfection; the goal is structural fidelity and readable Markdown.

Tables need extra scrutiny. Direct conversion is often unreliable for:

- `tabularx`, `tabular*`, `multirow`, `multicolumn`, `cmidrule`
- grouped headers and grouped row labels
- inline icons or `\includegraphics` cells
- model names wrapped in `\mbox`, `\small`, or nested math text

If Markdown Preview Enhanced stability matters, prefer pure Markdown tables over retained HTML tables. Validate grouped labels and row order against the source TeX after cleanup.

Appendix prompt sections also need special handling. When a converter produces giant three-column tables full of escaped `\n` content, prefer expanding them into per-item Markdown blocks:

- one heading per benchmark or backbone
- one fenced code block for the prompt
- one fenced code block for the example

This is often more readable and more stable in Markdown Preview Enhanced than forcing everything into a wide Markdown table.

### 7. Validate Before Handing Off

Before finishing, audit the Markdown for unresolved references and numbering drift.

Run the bundled script:

```bash
python3 scripts/audit_refs.py /absolute/path/to/paper.md
```

Use it to detect:

- referenced figure/table/algorithm numbers with no matching caption
- caption numbers that are never referenced
- missing internal link targets such as `(#fig:...)` with no matching `<a id="fig:..."></a>`
- duplicate explicit anchors that would make internal navigation ambiguous
- unresolved label tokens such as `[fig:...]`, `[tab:...]`, `[alg:...]`
- residue such as `Figure.` or `*Caption:`
- HTML wrappers such as `<table>`, `<div class="table*">`, `<span>`, `<figure>`, `<embed>`
- duplicated prose prefixes such as `Figure Figure 3` or `Table Table 2`

Important limitation:

- `scripts/audit_refs.py` is heuristic
- it is best at catching missing captions, unresolved labels, HTML residue, and duplicated prefixes
- it may undercount references when the file still uses numeric internal links instead of explicit prose like `Figure 7`
- it may also expose real caption gaps after prose cleanup, so do not assume a readable file is already numbered correctly
- if the audit output says captions exist but prose refs are missing, manually inspect whether the document uses linked numeric references rather than treating the audit as ground truth

Then manually inspect any reported mismatch.

For the exact cleanup checklist, read [references/normalization-checklist.md](references/normalization-checklist.md).
For recurring failure modes and the preferred fallback path, read [references/failure-modes.md](references/failure-modes.md).

## Practical Rules

- Preserve the extracted TeX source tree as the high-fidelity archive
- Treat Markdown as a calibrated derivative artifact
- Prefer relative image paths
- Prefer explicit numbered captions over implicit visual ordering
- Prefer stable explicit anchors over renderer-guessed heading ids when the file has many internal references
- Do not claim alignment with the TeX output unless numbering and references were checked
- Do not treat "reads smoothly in Markdown" as evidence that figure and table numbering is aligned
- If MPE cannot render a figure inline, convert the asset rather than expecting PDF embedding to work
- If a complex table still looks suspicious after conversion, trust the source TeX over the generated Markdown and rewrite the table

## Deliverable Standard

A paper is "done" only when:

- the Markdown opens cleanly in Markdown Preview Enhanced
- figures render inline
- each textual `Figure N` / `Table N` / `Algorithm N` can be located directly in the Markdown
- each internal `(#...)` link target resolves to a matching explicit anchor when such links are present
- unresolved labels are removed or replaced
- obvious HTML conversion residue is gone
- only intentional anchor tags remain, if any
- complex tables no longer contain parse-breaking TeX or HTML residue
- the source tree and rendered assets remain available locally
