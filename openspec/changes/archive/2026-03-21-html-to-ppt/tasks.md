## 1. Dependencies

- [x] 1.1 Install `python-pptx`, `beautifulsoup4`, `lxml`, and `requests` via pip (or add to requirements.txt)

## 2. Core Python Script

- [x] 2.1 Create `html_to_ppt.py` with CLI entry point accepting `--input` (file path or `-` for stdin) and `--output` arguments
- [x] 2.2 Implement HTML loading: read from file path or accept raw HTML string
- [x] 2.3 Implement BeautifulSoup HTML parsing and heading-based slide segmentation (h1/h2 → new slide)
- [x] 2.4 Implement slide title mapping from heading text
- [x] 2.5 Implement body content mapping: paragraphs → text, ul/ol li → bullet points
- [x] 2.6 Implement local image embedding into slides (skip with stderr warning if path missing)
- [x] 2.7 Implement default output path logic (input filename with `.pptx` extension)
- [x] 2.8 Write output `.pptx` file using `python-pptx`

## 3. skill.md

- [x] 3.1 Create `skill.md` with skill name, description, input parameters, output description, and example invocations for agent/LLM use

## 4. Validation

- [x] 4.1 Test conversion with a sample HTML file containing h1, h2, p, ul, and an img tag
- [x] 4.2 Verify output `.pptx` opens correctly in PowerPoint or LibreOffice Impress
- [x] 4.3 Verify skill.md accurately reflects the script's interface
