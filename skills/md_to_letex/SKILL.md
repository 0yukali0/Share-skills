---
name: md_to_letex
description: Convert a Markdown (.md) source file into a LaTeX (.tex) document. Use when the user wants to convert Markdown to LaTeX, or as a first step before compiling to PDF with the letex_to_pdf skill.
license: Apache License 2.0
metadata:
  author: yuteng
  version: "1.0"
---

## Goals
Convert a Markdown source file (`.md`) into a standalone LaTeX document (`.tex`) using the `pandoc` Python package.

## Steps
1. Execute `flyte run --local skill_impl/md_to_letex/md_to_letex.py md_to_letex --src <來源.md> --output <輸出.tex>`
2. Display the output path from the result.

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--src`   | Yes      | Path to the `.md` Markdown source file |
| `--output`| Yes      | Output `.tex` file path |

## Example Invocations

**Convert a Markdown file to LaTeX:**
```
Execute command: flyte run --local skill_impl/md_to_letex/md_to_letex.py md_to_letex --src report.md --output report.tex
```

**Full pipeline — Markdown to PDF:**
```
Execute command: flyte run --local skill_impl/md_to_letex/md_to_letex.py md_to_letex --src report.md --output report.tex
Execute command: flyte run --local skill_impl/letex_to_pdf/letex_to_pdf.py letex_to_pdf --src report.tex --output report.pdf
```

## Example Output
```
Saved: report.tex
```

## Notes
- The output `.tex` file is a standalone document with `\documentclass` preamble, suitable for direct compilation with `xelatex` or `pdflatex`.
- Requires `pandoc` binary to be installed on the system (`sudo apt install pandoc` or `brew install pandoc`).
- UTF-8 encoding is used for both input and output.
