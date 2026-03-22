## Context

The project already has a `letex_to_pdf` skill that compiles `.tex` to PDF. Authors who write in Markdown need a preceding step to convert `.md` to `.tex`. The `pandoc` Python package provides a clean Python API for this conversion and is added as a project dependency via `uv add pandoc`.

The implementation follows the same Flyte task pattern used by `letex_to_pdf` and `html_to_ppt`: a single `@env.task`-decorated function with `src` and `output` string parameters.

## Goals / Non-Goals

**Goals:**
- Convert a Markdown file to a LaTeX `.tex` file using the `pandoc` Python package
- Follow the existing `flyte run --local` invocation pattern
- Add `pandoc` to `pyproject.toml` via `uv add pandoc`
- Provide an agent-callable `SKILL.md`

**Non-Goals:**
- Chaining with `letex_to_pdf` (each skill is standalone)
- Supporting stdin or URL inputs
- Custom LaTeX template customization in this iteration

## Decisions

**Use the `pandoc` Python package (not subprocess)**
The `pandoc` PyPI package provides a Python-native API (`pandoc.read` / `pandoc.write`) and requires the `pandoc` binary to be present. Since the Flyte task environment is a local process, the system pandoc binary is used directly via the package. This keeps the code idiomatic and avoids raw subprocess calls.

Alternative considered: `pypandoc` — similar capability, but `pandoc` has a cleaner API and the user specified this package.

**Flyte TaskEnvironment with no extra apt packages**
The `pandoc` Python package delegates to the system `pandoc` binary. Since this runs `--local`, the user is expected to have `pandoc` installed on their machine (same expectation as `pdflatex` for the existing `letex_to_pdf` skill). If the binary is missing, a clear error is printed.

**Output format: LaTeX (`latex`)**
`pandoc` supports multiple LaTeX output formats (`latex`, `beamer`, `context`). Plain `latex` is the default and produces a standalone `.tex` file with `\documentclass` preamble, suitable for further compilation with `xelatex`.

## Risks / Trade-offs

- [pandoc binary not installed] → Print a clear error message with install instructions; do not silently produce empty output
- [Encoding issues with CJK/special characters] → pandoc handles UTF-8 by default; no extra flags needed
- [Large Markdown files] → pandoc is fast; no significant performance concern for typical document sizes

## Migration Plan

No migration needed. This is a net-new skill with no modifications to existing files.
