## ADDED Requirements

### Requirement: Convert Markdown to LaTeX
The system SHALL convert a Markdown source file to a LaTeX `.tex` file using the `pandoc` Python package.

#### Scenario: Successful conversion
- **WHEN** the user runs `flyte run --local skill_impl/md_to_letex/md_to_letex.py md_to_letex --src doc.md --output doc.tex`
- **THEN** a valid LaTeX file is written to the specified output path and the output path is printed

#### Scenario: Missing source file
- **WHEN** the `--src` path does not exist
- **THEN** the task exits with an error message indicating the file was not found

#### Scenario: pandoc binary not available
- **WHEN** the `pandoc` binary is not installed on the system
- **THEN** the task exits with a clear error message instructing the user to install pandoc

### Requirement: Standalone LaTeX output
The generated `.tex` file SHALL be a standalone document including `\documentclass` preamble, suitable for direct compilation with `xelatex` or `pdflatex`.

#### Scenario: Output is standalone LaTeX
- **WHEN** conversion completes successfully
- **THEN** the output `.tex` file contains `\documentclass` and can be compiled by the `letex_to_pdf` skill

### Requirement: Agent-callable SKILL.md
The skill SHALL be described in `skills/md_to_letex/SKILL.md` with inputs, outputs, and invocation examples so an AI agent can invoke it without additional context.

#### Scenario: Skill invoked by agent
- **WHEN** an agent reads `skills/md_to_letex/SKILL.md` and follows the invocation example
- **THEN** the correct `flyte run --local` command is executed with the user-supplied `--src` and `--output` arguments
