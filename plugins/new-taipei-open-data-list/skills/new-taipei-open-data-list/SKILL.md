---
name: new-taipei-open-data-list
description: This skill should be used when the user asks to "查詢新北市開放資料", "列出新北市資料集", "新北開放資料有哪些", or wants to browse or filter New Taipei City Open Data datasets by category.
version: 1.0.0
---

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `category` | No | 主題分類名稱，例如 `交通`、`環境`、`教育`；不填則回傳全部資料集 |

# New Taipei City Open Data List Skill

當使用者要查詢新北市開放資料集清單時，依序執行以下步驟：

## 步驟 1 — 確認輸入

從使用者的描述中判斷：
- `category`：主題分類名稱（可選，不填則輸出全部）

## 步驟 2 — 執行指令

使用 Bash tool 在 `plugins/new-taipei-open-data-list/skills/new-taipei-open-data-list/` 目錄下執行：

**不帶主題（回傳全部）：**
```bash
uv sync --locked && source .venv/bin/activate && flyte run --local ../../commands/new_taipei_open_data_list.py new_taipei_open_data_list
```

**帶主題篩選：**
```bash
uv sync --locked && source .venv/bin/activate && flyte run --local ../../commands/new_taipei_open_data_list.py new_taipei_open_data_list --category "交通"
```

## 步驟 3 — 回報結果

告知使用者查詢到的資料集清單，說明資料集總數及主題（若有篩選）。
