---
name: create-mindmap
description: This skill should be used when the user asks to "create a mindmap", "generate a mindmap", "draw a mindmap", or wants to visualize structured information as a mindmap diagram.
version: 1.0.0
---

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `topic` | Yes | 心智圖的根節點主題 |
| `items` | Yes | JSON 格式的子節點列表，支援字串與巢狀 dict，例如 `'["A", "B", {"C": ["C1", "C2"]}]'` |
| `output_path` | No | 輸出 PNG 檔案路徑，預設 `mindmap.png` |

# Create Mindmap Skill

當使用者要求產生心智圖時，依序執行以下步驟：

## 步驟 1 — 確認輸入

從使用者的描述中擷取：
- `topic`：心智圖主題
- `items`：子節點結構（JSON 格式字串）
- `output_path`：輸出路徑（可選，預設 `mindmap.png`）

## 步驟 2 — 執行指令

使用 Bash tool 在 `plugins/create-mindmap-plugin/skills/create-mindmap/` 目錄下執行：

```bash
uv sync --locked && source .venv/bin/activate && flyte run --local ../../commands/create_mindmap.py create_mindmap --topic "<topic>" --items '<items_json>' --output_path "<output_path>"
```

## 步驟 3 — 回報結果

告知使用者 PNG 圖片已產生於指定路徑，並顯示產生的 Mermaid 語法供參考。
