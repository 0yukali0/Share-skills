### Requirement: Compile LaTeX source to PDF
The system SHALL accept a `.tex` source file path and an output `.pdf` path and produce a compiled PDF document.

#### Scenario: Successful compilation
- **WHEN** `letex_to_pdf` is called with a valid `.tex` file path and an output path
- **THEN** a `.pdf` file SHALL be created at the specified output path

#### Scenario: Two-pass compilation
- **WHEN** the `.tex` source contains cross-references or a table of contents
- **THEN** `xelatex` SHALL be run twice to resolve them correctly

### Requirement: Blank PDF on compilation error
The system SHALL generate a blank single-page PDF at the output path when `xelatex` fails to produce a PDF.

#### Scenario: Compilation fails with no PDF output
- **WHEN** `xelatex` exits with a non-zero exit code and no PDF is produced
- **THEN** a blank PDF SHALL be written to the output path
- **THEN** a warning message with the xelatex error details SHALL be printed to stderr

#### Scenario: Compilation exits non-zero but PDF exists
- **WHEN** `xelatex` exits with a non-zero exit code but a PDF was still produced
- **THEN** the produced PDF SHALL be copied to the output path
- **THEN** a warning message SHALL be printed to stderr

### Requirement: Compile in a temporary directory
The system SHALL run `xelatex` in a temporary directory to avoid polluting the source directory with auxiliary files.

#### Scenario: Auxiliary files not left behind
- **WHEN** compilation completes (success or failure)
- **THEN** `.aux`, `.log`, `.toc` and other auxiliary files SHALL NOT remain in the source file's directory

### Requirement: SKILL.md agent interface
The system SHALL include a `SKILL.md` describing the skill name, inputs, outputs, and example invocations for agent use.

#### Scenario: SKILL.md contains required sections
- **WHEN** an agent reads `skills/letex_to_pdf/SKILL.md`
- **THEN** it SHALL contain: skill name, description, `--src` and `--output` parameter docs, and at least one example invocation using `flyte run --local`
