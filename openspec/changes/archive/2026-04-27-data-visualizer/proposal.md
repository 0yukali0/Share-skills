## Why

使用者有時需要快速將開放資料（CSV / JSON）以視覺化方式呈現，目前流程需手動撰寫圖表程式碼，耗時且缺乏一致性。此 plugin 讓 Claude 自動分析資料欄位並選擇適合的圖表類型，透過 Gradio gr.HTML 產生互動式視覺化，並以 Playwright 驗證結果，大幅降低使用者門檻。

## What Changes

- 新增 `data-visualizer` plugin，置於 `plugins/data-visualizer/`
- plugin 結構參考 `taipei-open-data-list`：
  - `commands/pyproject.toml` — 依賴包含 `gradio`
  - `commands/uv.lock` — 鎖定依賴版本
  - `skills/data-visualizer/SKILL.md` — 描述 Claude 執行視覺化的完整步驟
- Skill 步驟涵蓋：從使用者取得有效連結、欄位分析與圖表選型、使用 `gr.HTML` 建立視覺化、啟動 Gradio server 並以 Playwright 驗證

## Capabilities

### New Capabilities

- `data-visualizer`: 從使用者提供的資料連結（List[str]）自動分析欄位、選擇圖表類型（柱狀圖、折線圖、熱力圖等），以 Gradio gr.HTML 呈現，並透過 Playwright 自動化驗證視覺化是否正常運作

### Modified Capabilities

## Impact

- 新增 `plugins/data-visualizer/` 目錄（commands + skills）
- 依賴新增：`gradio`（透過 pyproject.toml + uv.lock）
- 不影響現有 plugin
