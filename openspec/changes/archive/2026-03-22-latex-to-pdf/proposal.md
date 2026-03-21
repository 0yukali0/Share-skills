## Why

Compiling LaTeX documents to PDF is a common need for generating typeset reports, papers, and documents. This skill provides a Flyte-based Python script and an agent-callable `SKILL.md` for programmatic LaTeX-to-PDF conversion.

## What Changes

- Add `skill_imple/letex_to_pdf/letex_to_pdf.py` — Flyte task that compiles a `.tex` source file to `.pdf` using `pdflatex`
- Add `skills/letex_to_pdf/SKILL.md` — agent-callable skill definition with inputs, outputs, and invocation examples
- No existing files modified

## Capabilities

### New Capabilities
- `latex-to-pdf`: Accepts a `.tex` source path and an output `.pdf` path, compiles the document using `pdflatex` via subprocess, and returns the path of the generated PDF

### Modified Capabilities

## Impact

- New files: `skill_imple/letex_to_pdf/letex_to_pdf.py`, `skills/letex_to_pdf/SKILL.md`
- System dependency: `pdflatex` must be available in PATH (from TeX Live or MiKTeX)
- No new Python package dependencies (uses `subprocess` from stdlib)
- Invocation: `flyte run --local skill_imple/letex_to_pdf/letex_to_pdf.py letex_to_pdf --src <source.tex> --output <output.pdf>`
