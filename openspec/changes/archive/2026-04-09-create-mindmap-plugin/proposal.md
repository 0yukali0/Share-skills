## Why

目前專案缺乏將文字內容自動轉換為心智圖（mindmap）的能力。使用者經常需要將複雜的資訊結構化為視覺化的心智圖來輔助理解與溝通，手動繪製費時費力。透過 plugin 自動產生 Mermaid 語法並轉換為 PNG 圖片，可大幅提升效率。

## What Changes

- 新增 `create-mindmap-plugin` plugin，遵循現有 plugin 結構（commands/ + skills/）
- 新增 `create_mindmap.py` command，包含兩個核心函數：
  - `gen_mindmap_mermaid`：接收主題與內容，產出 Mermaid mindmap 語法結構
  - `mermaid_to_png`：將 Mermaid 語法轉換為 PNG 圖片檔案
- 新增 `test_create_mindmap.py` 測試檔案，使用 pytest 對兩個函數進行單元測試
- 新增 `SKILL.md` 描述此 skill 的使用方式與觸發條件
- 更新 `.claude-plugin/marketplace.json` 註冊新 plugin

## Capabilities

### New Capabilities
- `mindmap-generation`: 從文字輸入產生 Mermaid mindmap 語法結構並輸出為 PNG 圖片

### Modified Capabilities

（無既有 capability 需要修改）

## Impact

- 新增 `plugins/create-mindmap-plugin/` 目錄及其下 commands/、skills/ 子結構
- 依賴：需要 mermaid CLI（`@mermaid-js/mermaid-cli` 或 `mmdc`）來將 Mermaid 轉為 PNG
- 依賴：需要 pytest 進行測試
- 更新 `plugins/.claude-plugin/marketplace.json` 加入新 plugin 條目
