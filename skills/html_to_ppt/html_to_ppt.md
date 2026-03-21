## Skill: html-to-ppt

Convert an HTML file or HTML string into a PowerPoint (.pptx) presentation.

## When to Use

Use this skill when the user wants to:
- Convert a web page or HTML document into a slide deck
- Turn an HTML report, article, or document into a PowerPoint file
- Generate a `.pptx` from structured HTML content

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--input` / `-i` | Yes | Path to the HTML file, or `-` to read from stdin |
| `--output` / `-o` | No | Output `.pptx` file path. Defaults to input filename with `.pptx` extension |

## Output

A `.pptx` file where:
- Each `<h1>` or `<h2>` heading becomes a new slide title
- `<p>` paragraphs and `<ul>`/`<ol>` list items become slide body content and bullets
- Local `<img>` references are embedded into the slide
- Remote or missing images are skipped with a warning

## Steps

1. Execute `uv run python html_to_ppt.py --input <path_to_html> --output <path_to_pptx>`

## Example Invocations

**Convert a local HTML file:**
```
Execute command: uv run python html_to_ppt.py --input report.html --output report.pptx
```

**Convert with default output path (report.html → report.pptx):**
```
Execute command: uv run python html_to_ppt.py --input report.html
```

**Convert from stdin:**
```
Execute command: cat page.html | uv run python html_to_ppt.py --input - --output slides.pptx
```

## Example Output

```
Saved: report.pptx (5 slides)
```

## Notes

- Only static HTML is supported (no JavaScript-rendered content)
- Complex layouts (tables, nested divs) are flattened to plain text
- Only local image paths are embedded; remote URLs require `requests` and are fetched automatically
