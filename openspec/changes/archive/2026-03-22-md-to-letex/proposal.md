## Why

Converting Markdown documents to LaTeX is a common need when authors write in Markdown but need typeset output for academic papers, reports, or further PDF compilation. This skill complements the existing `letex_to_pdf` skill to form a full Markdown → LaTeX → PDF pipeline.

## What Changes

- Add `skill_impl/md_to_letex/md_to_letex.py` — Flyte task that converts a `.md` source file to a `.tex` LaTeX document using the `pandoc` Python package
- Add `skills/md_to_letex/SKILL.md` — agent-callable skill definition with inputs, outputs, and invocation examples
- Add `pandoc` as a project dependency via `uv add pandoc`
- No existing files modified

## Capabilities

### New Capabilities
- `md-to-letex`: Accepts a Markdown source path and an output `.tex` path, converts the document using the `pandoc` Python package, and returns the path of the generated LaTeX file

### Modified Capabilities

## Impact

- New files: `skill_impl/md_to_letex/md_to_letex.py`, `skills/md_to_letex/SKILL.md`
- New Python dependency: `pandoc` (installed via `uv add pandoc`)
- Invocation: `flyte run --local skill_impl/md_to_letex/md_to_letex.py md_to_letex --src <source.md> --output <output.tex>`
