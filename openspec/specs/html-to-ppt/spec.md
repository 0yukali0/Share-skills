### Requirement: Convert HTML file to PowerPoint
The system SHALL accept a path to an HTML file and produce a `.pptx` output file by parsing the HTML structure and mapping it to slides.

#### Scenario: Basic HTML file conversion
- **WHEN** the script is called with a valid HTML file path
- **THEN** a `.pptx` file SHALL be created at the specified output path

#### Scenario: Default output path
- **WHEN** no output path is specified
- **THEN** the output file SHALL be named after the input file with a `.pptx` extension in the same directory

### Requirement: Accept raw HTML string input
The system SHALL accept a raw HTML string (in addition to a file path) as input for conversion.

#### Scenario: Raw HTML string input
- **WHEN** the script is called with a raw HTML string and an output path
- **THEN** a `.pptx` file SHALL be created at the specified output path

### Requirement: Map headings to slide titles
The system SHALL treat each `<h1>` and `<h2>` element as the start of a new slide, using the heading text as the slide title.

#### Scenario: h1 starts a new slide
- **WHEN** an `<h1>` element is encountered
- **THEN** a new slide SHALL be created with that heading as its title

#### Scenario: h2 starts a new slide
- **WHEN** an `<h2>` element is encountered
- **THEN** a new slide SHALL be created with that heading as its title

### Requirement: Map paragraphs and lists to slide body content
The system SHALL collect `<p>`, `<ul>`, and `<ol>` elements following a heading and add them as body text or bullet points on the corresponding slide.

#### Scenario: Paragraph after heading becomes body text
- **WHEN** a `<p>` element follows a heading
- **THEN** its text SHALL appear in the slide body

#### Scenario: Unordered list items become bullets
- **WHEN** a `<ul>` with `<li>` items follows a heading
- **THEN** each list item SHALL appear as a bullet point in the slide body

### Requirement: Embed local images
The system SHALL embed images referenced by local file paths in `<img>` tags into the slide.

#### Scenario: Local image embedded
- **WHEN** an `<img>` tag references a local file path that exists
- **THEN** the image SHALL be embedded in the corresponding slide

#### Scenario: Missing image skipped with warning
- **WHEN** an `<img>` tag references a path that does not exist
- **THEN** the image SHALL be skipped and a warning SHALL be printed to stderr

### Requirement: skill.md describes the agent interface
The system SHALL include a `skill.md` file that documents the skill name, description, inputs, outputs, and example invocations for agent/LLM use.

#### Scenario: skill.md contains required sections
- **WHEN** a developer or agent reads `skill.md`
- **THEN** it SHALL contain: skill name, description, input parameters, output description, and at least one example invocation
