## 1. Project Setup

- [x] 1.1 Create directory `skill_impl/letex_to_pdf/`
- [x] 1.2 Add `fpdf2` dependency via `uv add fpdf2`

## 2. Core Flyte Task

- [x] 2.1 Create `skill_impl/letex_to_pdf/letex_to_pdf.py` with `flyte.TaskEnvironment` setup
- [x] 2.2 Implement `letex_to_pdf(src: str, output: str)` Flyte task that copies the `.tex` file into a temp directory and runs `pdflatex` twice via `subprocess`
- [x] 2.3 On successful compilation, copy the output `.pdf` from temp dir to `output` path
- [x] 2.4 On compilation error (non-zero exit), generate a blank single-page PDF at `output` using `fpdf2` and print a warning to stderr

## 3. SKILL.md

- [x] 3.1 Create directory `skills/letex_to_pdf/`
- [x] 3.2 Create `skills/letex_to_pdf/SKILL.md` with YAML frontmatter, description, `--src`/`--output` parameter docs, and example invocations

## 4. Validation

- [x] 4.1 Test with a minimal valid `.tex` file — verify `.pdf` is produced
- [x] 4.2 Test with an invalid `.tex` file — verify blank PDF is produced and warning is printed to stderr
- [x] 4.3 Verify auxiliary files (`.aux`, `.log`) are not left in the source directory
