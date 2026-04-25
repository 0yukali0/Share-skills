## Why

台北市開放資料查詢 Plugin（taipei-open-data-list）已成功上線，但目前尚無新北市版本。新北市亦提供公開資料 API，資料結構與台北市相似，有必要建立對等的 Plugin 以支援新北市資料查詢需求。

## What Changes

- 新增 `new-taipei-open-data-list` Claude Code Plugin，提供查詢新北市開放資料集清單的能力
- 資料來源：`https://data.ntpc.gov.tw/api/datasets/info/json`
- 支援依「主題分類」篩選資料集，回傳「資料集名稱」清單
- 結構與 `taipei-open-data-list` Plugin 一致（Flyte task + SKILL.md + uv 環境）

## Capabilities

### New Capabilities

- `new-taipei-open-data-list`：查詢新北市開放資料集清單，支援可選的主題分類篩選，回傳資料集名稱 `List[str]`

### Modified Capabilities

（無現有 capability 需修改）

## Impact

- 新增 `plugins/new-taipei-open-data-list/` 目錄（commands + skills 結構）
- 新增 `plugins/.claude-plugin/marketplace.json` 中的 plugin 登錄項目
- 依賴：`httpx`、`flyte`（與 taipei-open-data-list 相同）
- 不影響現有 Plugin 或 specs
