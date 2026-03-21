---
name: letex_to_pdf
description: Compile a LaTeX (.tex) source file into a PDF. Use when the user wants to convert a LaTeX document to PDF format.
license: Apache License 2.0
metadata:
  author: yuteng
  version: "1.0"
---

## Goals
Compile a LaTeX source file (`.tex`) into a PDF document using `pdflatex`. If compilation fails, an empty PDF is produced and a warning is shown.

## Steps
1. Execute `flyte run --local skill_impl/letex_to_pdf/letex_to_pdf.py letex_to_pdf --src <來源.tex> --output <輸出.pdf>`
2. Display the output path from the result.

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--src`   | Yes      | Path to the `.tex` source file |
| `--output`| Yes      | Output `.pdf` file path |

## Example Invocations

**Compile a LaTeX file:**
```
Execute command: flyte run --local skill_impl/letex_to_pdf/letex_to_pdf.py letex_to_pdf --src report.tex --output report.pdf
```

## Example Output
```
Saved: report.pdf
```

## Notes
- `pdflatex` is run twice to resolve cross-references and table of contents.
- If compilation fails, a blank PDF is written to the output path and an error warning is printed.
- Auxiliary files (`.aux`, `.log`, etc.) are not left in the source directory.
