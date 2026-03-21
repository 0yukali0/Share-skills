---
name: html_to_ppt
description: Convert html which is provided to ppt format.
license: Apache License 2.0
metadata:
  author: yuteng
  version: "1.0"
---

Convert an HTML file or HTML string into a PowerPoint (.pptx) presentation.

## When to Use

Use this skill when the user wants to:
- Convert a web page or HTML document into a slide deck
- Turn an HTML report, article, or document into a PowerPoint file
- Generate a `.pptx` from structured HTML content

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--src` | Yes | Path to the HTML file, or `-` to read from stdin |
| `--output` | No | Output `.pptx` file path. Defaults to input filename with `.pptx` extension |

## Output

A `.pptx` file where:
- Each `<h1>` or `<h2>` heading becomes a new slide title
- `<p>` paragraphs and `<ul>`/`<ol>` list items become slide body content and bullets
- Local `<img>` references are embedded into the slide
- Remote or missing images are skipped with a warning

## Steps

1. Execute `flyte run --local skill_impl/html_to_ppt/html_to_ppt.py html_to_ppt --src <path_to_html> --output <path_to_pptx>`

## Example Invocations

**Convert a local HTML file:**
```
Execute command: flyte run --local skill_impl/html_to_ppt/html_to_ppt.py html_to_ppt --src report.html --output report.pptx
```

**Convert with default output path (report.html → report.pptx):**
```
Execute command: flyte run --local skill_impl/html_to_ppt/html_to_ppt.py html_to_ppt --src report.html
```

**Convert from stdin:**
```
Execute command: flyte run --local skill_impl/html_to_ppt/html_to_ppt.py html_to_ppt --src - --output slides.pptx
```

## Example Output

```
Saved: report.pptx (5 slides)
```

## Notes

- Only static HTML is supported (no JavaScript-rendered content)
- Complex layouts (tables, nested divs) are flattened to plain text
- Only local image paths are embedded; remote URLs require `requests` and are fetched automatically
