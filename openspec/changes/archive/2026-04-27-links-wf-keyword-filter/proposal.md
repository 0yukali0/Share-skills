## Why

`links_wf` 目前回傳所有資料集的連結，無法針對特定主題過濾。使用者需要依關鍵字快速找到相關資料集名稱與下載連結。同時 SKILL.md 說明文件的行文風格與現有內容不一致，需一併統一。

## What Changes

- 新增 `keyword_links_wf(urls, keyword)` task：接受 API_URLS 與關鍵字字串，回傳資料集名稱包含關鍵字的 `Dict[str, str]`（名稱→連結）
- 更新 SKILL.md：補充 `keyword_links_wf` 使用說明，並統一全文行文風格（繁體中文、表格格式與指令區塊對齊）

## Capabilities

### New Capabilities

- `keyword-links-wf`: 依關鍵字過濾資料集並回傳對應連結的 workflow task

### Modified Capabilities

- （無）

## Impact

- `plugins/taipei-open-data-list/commands/wf.py`：新增 `keyword_links_wf` task
- `plugins/taipei-open-data-list/skills/taipei-open-data-list/SKILL.md`：更新說明文件
