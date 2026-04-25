## Why

台北市開放資料平台擁有大量資料集，使用者難以快速查詢特定主題的資料集清單。此 plugin 讓 Claude 能直接從台北市開放資料 API 取得最新資料集目錄，並依主題分類篩選輸出，降低手動瀏覽平台的成本。

## What Changes

- 新增 `taipei-open-data-list` plugin，結構與 `create-mindmap-plugin` 一致
  - `plugins/taipei-open-data-list/commands/taipei_open_data_list.py`：下載 API 資料並篩選輸出
  - `plugins/taipei-open-data-list/skills/taipei-open-data-list/SKILL.md`：Skill 說明文件
  - `plugins/taipei-open-data-list/skills/taipei-open-data-list/pyproject.toml`：Python 依賴設定
- 更新 `plugins/.claude-plugin/marketplace.json` 加入新 plugin 條目
- 從 `https://data.taipei/api/frontstage/tpeod/dataset.download?format=json` 下載資料集 JSON
- 擷取每筆資料的「資料集名稱」與「主題分類」欄位
- 支援依「主題分類」篩選，回傳 `List[str]` 格式資料集名稱；若未提供主題則輸出全部

## Capabilities

### New Capabilities

- `taipei-open-data-list`: 查詢台北市開放資料集清單，支援依主題分類篩選，回傳資料集名稱 `List[str]`

### Modified Capabilities

## Impact

- 新增 `plugins/taipei-open-data-list/` plugin 目錄（結構與 `create-mindmap-plugin` 相同）
- 更新 `plugins/.claude-plugin/marketplace.json`
- 需要 `httpx` 或 `requests` 套件（HTTP 請求）及 `flyte>=2.0.9`
- 不影響現有 plugin 或 skill
