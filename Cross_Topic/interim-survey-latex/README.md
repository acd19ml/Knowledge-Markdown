# Interim Survey LaTeX

This directory stores the LaTeX version of [interim-survey-draft.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/interim-survey-draft.md).

Files:

- `main.tex`: standalone LaTeX source generated from the Markdown draft
- `references.bib`: bibliography database used by `main.tex`

Notes:

- `main.tex` now uses `biblatex` with `backend=biber`
- the body still contains plain author-year mentions from the Markdown draft; the bibliography itself is now generated from `references.bib`
- to turn in a fully citation-managed LaTeX paper later, the next step would be replacing in-text mentions with `\textcite{...}` / `\parencite{...}` commands

Regenerate `main.tex` from the current Markdown source with:

```sh
tmp=$(mktemp /tmp/interim-survey.XXXXXX.md)
sed '1d;2,3d' Cross_Topic/interim-survey-draft.md > "$tmp"
pandoc "$tmp" --from gfm --to latex --standalone --shift-heading-level-by=-1 \
  --metadata title='Experience-Dependent Procedural Knowledge in GUI Agents: A Taxonomy and Research Agenda' \
  --metadata author='' --metadata date='' \
  -o Cross_Topic/interim-survey-latex/main.tex
rm -f "$tmp"
```

Compile with a LaTeX toolchain that supports `biber`, for example:

```sh
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```
