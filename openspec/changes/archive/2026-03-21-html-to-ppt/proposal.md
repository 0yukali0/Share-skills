## Why

Converting HTML content to PowerPoint presentations is a common need for generating slide decks from web content, reports, or documentation. This skill provides a reusable Python script and an agent-callable skill definition for programmatic HTML-to-PPT conversion.

## What Changes

- Add a Python script (`html_to_ppt.py`) that accepts HTML input and produces a `.pptx` file
- Add a `skill.md` describing the skill interface for agent/LLM invocation
- The script will parse HTML structure (headings, paragraphs, lists, images) and map them to PowerPoint slides and shapes

## Capabilities

### New Capabilities
- `html-to-ppt`: Converts HTML content into a PowerPoint (.pptx) file, mapping HTML structure to slides, titles, bullet points, and images

### Modified Capabilities

## Impact

- New dependency: `python-pptx` for PowerPoint generation, `beautifulsoup4` and `lxml` for HTML parsing
- New files: `html_to_ppt.py`, `skill.md`
- No existing code modified
