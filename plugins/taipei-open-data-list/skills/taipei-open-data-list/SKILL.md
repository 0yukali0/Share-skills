---
name: taipei-open-data-list
description: This skill should be used when the user asks to "查詢台北市/新北市開放資料", "列出台北市/新北市資料集", "台北開放資料有哪些", or wants to browse or filter Taipei/New Taipei Open Data datasets by category.
version: 3.0.0
---

## 輸入參數

| 參數 | 必填 | 說明 |
|------|------|------|
| `urls` | 否 | JSON 格式的城市→API URL 對照表；不填則同時查詢台北市與新北市 |

# Taipei Open Data List Skill

當使用者要查詢台北市或新北市開放資料集時，依需求選擇以下功能執行。

---

## 查詢資料集清單（describe_wf）

### 步驟 1 — 確認輸入

從使用者的描述中判斷要查詢哪個城市：

- 不指定：查詢兩市（使用預設值，不需傳 `--urls`）
- 僅台北市：`--urls '{"taipei": "https://data.taipei/api/frontstage/tpeod/dataset.download?format=json"}'`
- 僅新北市：`--urls '{"new-taipei": "https://data.ntpc.gov.tw/api/datasets/info/json"}'`

### 步驟 2 — 執行指令

在 `plugins/taipei-open-data-list/commands` 目錄下執行：

```bash
cd plugins/taipei-open-data-list/commands
UV_PROJECT_ENVIRONMENT=/tmp/.taipei-open-data-list-venv uv sync --locked && source /tmp/.taipei-open-data-list-venv/bin/activate
```

**查詢全部（兩市）：**
```bash
flyte run --local wf.py describe_wf
```

**僅查詢台北市：**
```bash
flyte run --local wf.py describe_wf --urls '{"taipei": "https://data.taipei/api/frontstage/tpeod/dataset.download?format=json"}'
```

**僅查詢新北市：**
```bash
flyte run --local wf.py describe_wf --urls '{"new-taipei": "https://data.ntpc.gov.tw/api/datasets/info/json"}'
```

### 步驟 3 — 回報結果

告知使用者查詢到的資料集清單，說明各城市的資料集總數。

---

## 取得資料集下載連結（links_wf）

回傳所有資料集的下載連結，格式為 `{資料集名稱: url}`。

```bash
cd plugins/taipei-open-data-list/commands
UV_PROJECT_ENVIRONMENT=/tmp/.taipei-open-data-list-venv uv sync --locked && source /tmp/.taipei-open-data-list-venv/bin/activate && flyte run --local wf.py links_wf
```

**僅查台北市：**
```bash
flyte run --local wf.py links_wf --urls '{"taipei": "https://data.taipei/api/frontstage/tpeod/dataset.download?format=json"}'
```

**僅查新北市：**
```bash
flyte run --local wf.py links_wf --urls '{"new-taipei": "https://data.ntpc.gov.tw/api/datasets/info/json"}'
```

連結格式：

- 台北市：`https://data.taipei/<資料存取網址>`（若已是完整 URL 則直接使用）
- 新北市：`https://data.ntpc.gov.tw/api/datasets/<識別碼>/<提供格式>`

---

## 依關鍵字查詢資料集連結（keyword_links_wf）

輸入關鍵字，回傳名稱包含該關鍵字的資料集連結，格式為 `{資料集名稱: url}`。關鍵字比對不區分大小寫。

| 參數 | 必填 | 說明 |
|------|------|------|
| `urls` | 否 | 城市→API URL 對照表；不填則查詢兩市 |
| `keyword` | 是 | 過濾用關鍵字（比對資料集名稱） |

**查詢含特定關鍵字的資料集：**
```bash
flyte run --local wf.py keyword_links_wf --keyword '交通'
```

**限定城市查詢：**
```bash
flyte run --local wf.py keyword_links_wf --urls '{"taipei": "https://data.taipei/api/frontstage/tpeod/dataset.download?format=json"}' --keyword '空氣品質'
```
