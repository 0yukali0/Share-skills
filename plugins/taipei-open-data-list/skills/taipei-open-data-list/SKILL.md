---
name: taipei-open-data-list
description: This skill should be used when the user asks to "查詢台北市/新北市開放資料", "列出台北市/新北市資料集", "台北開放資料有哪些", or wants to browse or filter Taipei/New Taipei Open Data datasets by category.
version: 3.0.0
---

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `urls` | No | JSON 格式的城市→API URL 對照表；不填則同時查詢台北市與新北市 |

# Taipei Open Data List Skill

當使用者要查詢台北市或新北市開放資料集清單時，依序執行以下步驟：

## 步驟 1 — 確認輸入

從使用者的描述中判斷要查詢哪個城市：
- 不指定：查詢兩市（使用預設值，不需傳 `--urls`）
- 僅台北市：`--urls '{"taipei": "https://data.taipei/api/frontstage/tpeod/dataset.download?format=json"}'`
- 僅新北市：`--urls '{"new-taipei": "https://data.ntpc.gov.tw/api/datasets/info/json"}'`

## 步驟 2 — 執行指令

使用 Bash tool 在 `plugins/taipei-open-data-list/commands` 目錄下執行：

**查詢全部（兩市）：**
```bash
uv sync --locked && source .venv/bin/activate && flyte run --local taipei_open_data_list.py taipei_open_data_list
```

**僅查詢台北市：**
```bash
uv sync --locked && source .venv/bin/activate && flyte run --local taipei_open_data_list.py taipei_open_data_list --urls '{"taipei": "https://data.taipei/api/frontstage/tpeod/dataset.download?format=json"}'
```

**僅查詢新北市：**
```bash
uv sync --locked && source .venv/bin/activate && flyte run --local taipei_open_data_list.py taipei_open_data_list --urls '{"new-taipei": "https://data.ntpc.gov.tw/api/datasets/info/json"}'
```

## 步驟 3 — 回報結果

告知使用者查詢到的資料集清單，說明各城市的資料集總數。
