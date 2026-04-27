## ADDED Requirements

### Requirement: Accept valid data links from user
The skill SHALL prompt the user to provide one or more data URLs (List[str]) and validate each link is accessible (HTTP 200) before proceeding. Supported formats are CSV and JSON.

#### Scenario: User provides valid CSV URL
- **WHEN** user provides a URL that returns HTTP 200 with Content-Type text/csv or file extension .csv
- **THEN** skill proceeds to field analysis with that URL

#### Scenario: User provides valid JSON URL
- **WHEN** user provides a URL that returns HTTP 200 with a JSON array or object body
- **THEN** skill proceeds to field analysis with that URL

#### Scenario: User provides inaccessible URL
- **WHEN** a URL returns non-200 status or connection error
- **THEN** skill informs the user and asks for a replacement URL before continuing

---

### Requirement: Analyze fields and select chart type
The skill SHALL fetch each data source, inspect the column names and data types, and select the most appropriate chart type according to these rules:
- Time-series columns (date/datetime) + numeric value → line chart
- Categorical column + numeric value → bar chart
- Two numeric columns with many rows → scatter chart
- Numeric matrix or correlation data → heatmap
- Proportion/composition → pie or donut chart

#### Scenario: Dataset has date and numeric columns
- **WHEN** dataset contains a column parseable as date/datetime and at least one numeric column
- **THEN** skill selects a line chart and maps date to x-axis, numeric to y-axis

#### Scenario: Dataset has categorical and numeric columns
- **WHEN** dataset contains a string/categorical column and a numeric column
- **THEN** skill selects a bar chart and maps categorical to x-axis, numeric to y-axis

#### Scenario: Dataset has two numeric columns
- **WHEN** dataset contains two or more numeric columns without a date column
- **THEN** skill selects a scatter chart by default

---

### Requirement: Build Gradio app using gr.HTML with embedded chart
The skill SHALL generate a Python script that creates a Gradio app with `gr.HTML` containing a self-contained HTML string. The HTML MUST embed a chart using Plotly CDN (https://cdn.plot.ly/plotly-latest.min.js) or Chart.js CDN. No additional Python charting libraries are required.

#### Scenario: Chart HTML is generated for bar chart
- **WHEN** skill selects bar chart for a dataset
- **THEN** generated script creates a `gr.HTML` component whose value contains a `<div>` with Plotly bar chart JavaScript using the fetched data

#### Scenario: Gradio app launches without error
- **WHEN** the generated script is run with `python app.py`
- **THEN** Gradio server starts on a specified port (default 7860) and returns HTTP 200 on the root path within 10 seconds

---

### Requirement: Verify visualization with Playwright
The skill SHALL use the playwright-skill to open the Gradio app URL in a headless browser, wait for the chart element to appear, take a screenshot, and confirm the chart rendered successfully. The Gradio server SHALL be stopped after verification.

#### Scenario: Chart element is visible in browser
- **WHEN** Playwright navigates to `http://localhost:<port>`
- **THEN** a `<div>` containing the chart SVG or canvas element is present in the DOM within 15 seconds

#### Scenario: Screenshot saved as verification artifact
- **WHEN** Playwright successfully renders the page
- **THEN** a screenshot is saved to `/tmp/data-visualizer-verify.png` and Claude reports the result to the user

#### Scenario: Verification fails
- **WHEN** Playwright cannot find the chart element within 15 seconds
- **THEN** skill reports the failure and the Gradio server logs to the user for debugging
