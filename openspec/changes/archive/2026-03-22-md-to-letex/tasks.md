## 1. Dependency Setup

- [x] 1.1 Run `uv add pandoc` to add the `pandoc` package to `pyproject.toml`

## 2. Python Implementation

- [x] 2.1 Create `skill_impl/md_to_letex/` directory
- [x] 2.2 Write `skill_impl/md_to_letex/md_to_letex.py` with a Flyte `@env.task` that reads the source `.md` file and uses `pandoc` to convert it to a standalone `.tex` file at the output path
- [x] 2.3 Handle missing source file with a clear error message
- [x] 2.4 Handle missing `pandoc` binary with an install hint error message
- [x] 2.5 Print `Saved: <output>` on success and return the output path

## 3. Skill Definition

- [x] 3.1 Create `skills/md_to_letex/` directory
- [x] 3.2 Write `skills/md_to_letex/SKILL.md` with frontmatter, goals, steps, inputs table, and example invocations following the pattern of `skills/letex_to_pdf/SKILL.md`

## 4. Verification

- [x] 4.1 Run `flyte run --local skill_impl/md_to_letex/md_to_letex.py md_to_letex --src <test.md> --output <test.tex>` and confirm the `.tex` file is created
- [x] 4.2 Optionally pipe the output into `letex_to_pdf` to verify end-to-end Markdown → PDF
