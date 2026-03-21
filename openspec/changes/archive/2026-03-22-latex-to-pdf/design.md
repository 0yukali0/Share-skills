## Context

The project uses a Flyte-based skill pattern: each skill is a Python file with `@TaskEnvironment.task` decorated functions, invoked via `flyte run --local`. Existing skills (`bbc_news`, `html_to_ppt`) follow this pattern. The `letex_to_pdf` skill follows the same conventions, using `subprocess` to shell out to `pdflatex`.

## Goals / Non-Goals

**Goals:**
- Implement `letex_to_pdf` as a Flyte task accepting `--src` (`.tex` file path) and `--output` (`.pdf` file path)
- Run `pdflatex` twice (for cross-references/TOC) in a temp directory, then copy the result to the output path
- On compilation error: generate a blank PDF at the output path and print a warning to stderr
- Provide `SKILL.md` describing the agent interface

**Non-Goals:**
- BibTeX/BibLaTeX bibliography compilation (no `bibtex`/`biber` pass)
- Remote `.tex` URLs or stdin input

## Decisions

### Subprocess over Python LaTeX libraries
`pdflatex` is the standard tool and already handles complex LaTeX features. `subprocess` is the correct layer.

### Two-pass compilation
Running `pdflatex` twice resolves internal references, table of contents, and labels correctly — standard practice.

### Compile in a temp directory
`pdflatex` produces auxiliary files (`.aux`, `.log`, `.toc`). Compiling in a `tempfile.TemporaryDirectory` keeps the workspace clean.

### Blank PDF on compilation error
When `pdflatex` exits with a non-zero code, generate a blank single-page PDF using `fpdf2` and write it to the output path. Print a warning with the pdflatex error to stderr. This ensures the output path always contains a valid PDF.

## Risks / Trade-offs

- **Blank PDF on error may be unexpected** → mitigated by stderr warning message with error details.
- **Large documents / long compile** → no timeout set; acceptable for local usage.
