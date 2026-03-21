## Context

HTML documents have a natural hierarchical structure (headings, paragraphs, lists, images) that maps well to PowerPoint slide structure (titles, content, bullet points). The goal is a standalone Python script plus a `skill.md` so agents can invoke the conversion capability via natural language or structured calls.

## Goals / Non-Goals

**Goals:**
- Parse HTML and extract meaningful structure (h1/h2 → slide titles, p/ul/ol → body content, img → images)
- Generate a `.pptx` file using `python-pptx`
- Provide a `skill.md` that describes the skill interface for agent invocation
- Support input as an HTML file path or raw HTML string
- Support configurable output path

**Non-Goals:**
- Full CSS styling fidelity (colors, fonts from inline CSS not fully reproduced)
- JavaScript-rendered content (static HTML only)
- Nested slide layouts beyond title + content
- Converting back from PPT to HTML

## Decisions

### HTML parsing: BeautifulSoup4
Chosen over raw regex or lxml directly because it handles malformed HTML gracefully and provides a clean traversal API.

### Slide mapping strategy: heading-based segmentation
Each `<h1>` or `<h2>` element starts a new slide. Title is the heading text; body collects subsequent `<p>`, `<ul>`, `<ol>`, and `<img>` until the next heading. This matches common document structure without requiring user annotation.

**Alternative considered:** One slide per top-level `<section>` tag — rejected because most HTML doesn't use semantic sections consistently.

### Output format: .pptx via python-pptx
Industry-standard library, well-maintained, no external services needed.

### skill.md format: Markdown with YAML frontmatter
Describes the skill name, description, inputs, outputs, and example invocations so agents can call the skill programmatically or via natural language.

## Risks / Trade-offs

- **Very long HTML pages** → many slides, potentially unwieldy deck. Mitigation: document the limitation; users should pre-filter content.
- **Images in HTML** → embedding requires downloading remote URLs. Mitigation: support local paths; remote URLs fetched with `requests`, skip if unavailable with a warning.
- **Complex HTML layouts** (tables, nested divs) → mapped to plain text with structure lost. Mitigation: document this limitation clearly in skill.md.
