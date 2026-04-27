---
name: data-visualizer
description: This skill should be used when the user wants to visualize data from URLs (CSV or JSON) using interactive charts. Claude fetches the data, analyzes the columns and content, decides the best chart type, generates a Gradio gr.HTML app with Plotly, and verifies the result with Playwright.
version: 2.0.0
---

## 輸入參數

| 參數 | 必填 | 說明 |
|------|------|------|
| `links` | 是 | 資料來源 URL 清單（List[str]），支援 CSV 與 JSON 格式 |

# Data Visualizer Skill

當使用者提供資料 URL 並想以圖表呈現時，由 **Claude 分析實際資料內容**、判斷最適合的圖表類型，再動態生成 Gradio 視覺化應用並驗證結果。

---

## 步驟 1 — 從使用者獲取有效的資料連結

向使用者詢問一或多個資料 URL（List[str]）。逐一驗證每個 URL 是否可存取：

```bash
cd plugins/data-visualizer/commands
UV_PROJECT_ENVIRONMENT=/tmp/.data-visualizer-venv uv sync --locked && source /tmp/.data-visualizer-venv/bin/activate
python - <<'EOF'
import httpx, json, csv, io

urls = [
    # 貼上使用者提供的 URLs
]

for url in urls:
    resp = httpx.get(url, timeout=20, follow_redirects=True, verify=False)
    print(f"{url[:60]} → {resp.status_code}, CT={resp.headers.get('content-type','')}")
EOF
```

若某個 URL 回傳非 200 或無法連線，告知使用者並請其提供替換連結。

---

## 步驟 2 — 讀取資料，由 Claude 分析欄位並決定圖表類型

對每個有效 URL，讀取實際資料（前 50 列）並由 Claude 觀察：

```bash
python - <<'EOF'
import httpx, json, csv, io

def fetch_sample(url, n=50):
    resp = httpx.get(url, timeout=30, follow_redirects=True, verify=False)
    ct = resp.headers.get("content-type", "")
    # JSON
    if "json" in ct or url.endswith(".json"):
        raw = resp.json()
        rows = raw if isinstance(raw, list) else raw.get("data", raw.get("records", [raw]))
        return rows[:n]
    # CSV（自動偵測 BIG-5 / UTF-8）
    for enc in (ct.split("charset=")[-1].strip() if "charset=" in ct else "utf-8", "big5", "utf-8-sig", "utf-8"):
        try:
            text = resp.content.decode(enc)
            return list(csv.DictReader(io.StringIO(text)))[:n]
        except Exception:
            continue
    return []

urls = [
    # 貼上使用者提供的 URLs
]

for url in urls:
    rows = fetch_sample(url)
    if rows:
        print(f"\nURL: {url[-50:]}")
        print(f"  欄位: {list(rows[0].keys())}")
        print(f"  範例第 1 列: {rows[0]}")
        print(f"  範例第 2 列: {rows[1] if len(rows) > 1 else 'N/A'}")
EOF
```

**Claude 根據以下觀察做出判斷：**

- 欄位名稱的語意（例如「年度」、「日期」→ 時間序列；「行政區」→ 類別）
- 欄位值的型態（數值、日期字串、類別字串）
- 資料的主題與分佈

**圖表選型參考：**

| 觀察到的特徵 | 推薦圖表 |
|---|---|
| 含日期/年度欄位 + 數值欄位 | 折線圖（Line） |
| 類別欄位（地區、名稱）+ 數值欄位 | 柱狀圖（Bar） |
| 兩個以上純數值欄位 | 散點圖（Scatter） |
| 數值矩陣 / 相關性 | 熱力圖（Heatmap） |
| 類別佔比 / 百分比 | 圓餅圖（Pie） |

> Claude 應根據實際資料語意做最終判斷，不限於上表規則。

---

## 步驟 3 — 使用 gr.HTML 建立視覺化：說明

Gradio 的 `gr.HTML` 接受一個 **HTML 字串**作為內容，可在其中嵌入完整的 Plotly JavaScript 圖表，不需要任何額外 Python 圖表套件。

基本結構：

```python
import gradio as gr

chart_inner = """
<div id="chart" style="width:100%;height:500px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
Plotly.newPlot('chart', [{ /* trace 資料 */ }], {
  title: '...',
  font: {family: "'Noto Sans TC', sans-serif"}
});
</script>
"""

# ⚠️ 重要：gr.HTML 用 innerHTML 設定內容，瀏覽器不執行動態插入的 <script>。
# 解法：用 base64 iframe 包裝，確保腳本正常執行且 CJK 字型正確顯示。
import base64

def iframe_wrap(inner_html: str, height: int = 500) -> str:
    full = f"""<!DOCTYPE html>
<html><head>
  <meta charset="utf-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC&display=swap" rel="stylesheet">
  <style>body{{margin:0;font-family:'Noto Sans TC',sans-serif}}</style>
</head><body>{inner_html}</body></html>"""
    encoded = base64.b64encode(full.encode()).decode()
    return f'<iframe src="data:text/html;base64,{encoded}" width="100%" height="{height}px" frameborder="0" style="border:none;"></iframe>'

with gr.Blocks(title="Data Visualizer") as demo:
    gr.HTML(value=iframe_wrap(chart_inner))

demo.launch(server_port=7860)
```

---

## 步驟 4 — 生成 app.py：將實際資料放入 gr.HTML

在 `plugins/data-visualizer/commands/app.py` 建立**針對此次資料量身訂製**的應用程式。

以下為 Claude 應生成的程式碼範本（根據步驟 2 的分析結果填入正確的欄位名稱與圖表類型）：

```python
import json
import gradio as gr
import httpx
import csv
import io

# --- 資料抓取（Claude 依分析結果決定解碼方式） ---
def fetch_data(url: str, encoding: str = "utf-8") -> list[dict]:
    resp = httpx.get(url, timeout=30, follow_redirects=True, verify=False)
    ct = resp.headers.get("content-type", "")
    if "json" in ct or url.endswith(".json"):
        raw = resp.json()
        return raw if isinstance(raw, list) else raw.get("data", raw.get("records", [raw]))
    for enc in (encoding, "big5", "utf-8-sig", "utf-8"):
        try:
            return list(csv.DictReader(io.StringIO(resp.content.decode(enc))))
        except Exception:
            continue
    return []

# --- 資料轉換為 Plotly HTML（Claude 依選型填入正確的 trace） ---
def build_html(data: list[dict], x_col: str, y_col: str, chart_type: str, title: str) -> str:
    x_vals = [str(row.get(x_col, "")) for row in data]
    y_vals = []
    for row in data:
        try:
            y_vals.append(float(str(row.get(y_col, 0)).replace(",", "")))
        except ValueError:
            y_vals.append(0)

    if chart_type == "pie":
        trace = f'{{"type":"pie","labels":{json.dumps(x_vals)},"values":{json.dumps(y_vals)}}}'
    elif chart_type == "line":
        trace = f'{{"type":"scatter","mode":"lines+markers","x":{json.dumps(x_vals)},"y":{json.dumps(y_vals)}}}'
    elif chart_type == "scatter":
        trace = f'{{"type":"scatter","mode":"markers","x":{json.dumps(x_vals)},"y":{json.dumps(y_vals)}}}'
    else:  # bar (default)
        trace = f'{{"type":"bar","x":{json.dumps(x_vals)},"y":{json.dumps(y_vals)}}}'

    inner = f"""
<div id="chart-main" style="width:100%;height:500px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
Plotly.newPlot('chart-main',[{trace}],{{
  title:"{title}",
  font:{{family:"'Noto Sans TC',sans-serif"}},
  xaxis:{{title:"{x_col}"}},
  yaxis:{{title:"{y_col}"}}
}});
</script>"""
    return iframe_wrap(inner)

# --- Gradio 應用（Claude 依分析結果填入 URL、欄位、圖表類型） ---
DATASETS = [
    # Claude 在此填入每個 URL 的設定
    # {"url": "...", "encoding": "big5", "x_col": "行政區", "y_col": "數值欄位", "chart_type": "bar", "title": "圖表標題"},
]

def build_all_charts() -> str:
    parts = []
    for ds in DATASETS:
        try:
            data = fetch_data(ds["url"], ds.get("encoding", "utf-8"))
            html = build_html(data, ds["x_col"], ds["y_col"], ds["chart_type"], ds["title"])
            parts.append(f"<h3>{ds['title']}</h3><p>資料筆數：{len(data)}</p>{html}<hr>")
        except Exception as e:
            parts.append(f"<p style='color:red'>Error: {e}</p>")
    return "".join(parts) if parts else "<p>無資料</p>"

with gr.Blocks(title="Data Visualizer") as demo:
    gr.Markdown("## Data Visualizer")
    chart_output = gr.HTML(value=build_all_charts())

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)
```

**Claude 需根據步驟 2 的分析填入 `DATASETS` 清單**，例如：

```python
DATASETS = [
    {
        "url": "https://data.taipei//api/dataset/.../download",
        "encoding": "big5",
        "x_col": "行政區",       # Claude 從欄位分析決定
        "y_col": "水患自主防災社區推動年度",  # Claude 從欄位分析決定
        "chart_type": "bar",    # Claude 判斷類別→柱狀圖
        "title": "台北市水患防災社區分佈",
    },
    {
        "url": "https://data.ntpc.gov.tw/api/datasets/.../json",
        "encoding": "utf-8",
        "x_col": "area",        # Claude 從欄位分析決定
        "y_col": "seqno",       # Claude 從欄位分析決定
        "chart_type": "bar",    # Claude 判斷類別→柱狀圖
        "title": "新北市資料集分佈",
    },
]
```

---

## 步驟 5 — 啟動並透過 Playwright 驗證

### 啟動 Gradio server

```bash
cd plugins/data-visualizer/commands
source /tmp/.data-visualizer-venv/bin/activate
python app.py &
APP_PID=$!
sleep 6
curl -s -o /dev/null -w "Server status: %{http_code}\n" http://localhost:7860
```

### 呼叫 playwright-skill 驗證

使用 `/playwright` skill，執行以下腳本（存至 `/tmp/verify_data_visualizer.js`）：

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('http://localhost:7860', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForSelector('.gradio-container', { timeout: 10000 });
  console.log('Page loaded:', await page.title());

  // 截圖儲存
  await page.screenshot({ path: '/tmp/data-visualizer-verify.png', fullPage: true });
  console.log('📸 截圖已儲存至 /tmp/data-visualizer-verify.png');

  // 確認圖表 div 存在
  const chartDiv = await page.locator('#chart-main').count();
  console.log(`chart-main div count: ${chartDiv}`);

  // 確認 Plotly script 已載入
  const plotlyScript = await page.locator('script[src*="plotly"]').count();
  console.log(`Plotly script tags: ${plotlyScript}`);

  await browser.close();
  console.log(chartDiv > 0 ? '✅ 驗證成功' : '⚠️  chart-main 未找到，請檢查 app.py');
})();
```

執行：

```bash
node /path/to/playwright-skill/run.js /tmp/verify_data_visualizer.js
```

### 驗證完成後關閉 server

```bash
kill $APP_PID 2>/dev/null || true
```

### 驗證成功標準

- `/tmp/data-visualizer-verify.png` 存在且截圖中可看到圖表
- `#chart-main` div 在 DOM 中存在
- Plotly script tag 已載入
