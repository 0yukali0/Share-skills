## Context

`taipei-open-data-list` Plugin 已建立完整的設計模式：Flyte task 封裝 API 呼叫、`uv` 管理 Python 環境、SKILL.md 定義 Claude Code 觸發條件。`new-taipei-open-data-list` 沿用相同架構，僅替換資料來源為新北市 Open Data API。

新北市 API 端點：`https://data.ntpc.gov.tw/api/datasets/info/json`  
回傳 JSON 陣列，每筆含「資料集名稱」與「主題分類」欄位（與台北市格式相同）。

## Goals / Non-Goals

**Goals:**
- 建立結構與 `taipei-open-data-list` 完全一致的新 Plugin
- 支援無參數（回傳全部）與帶 `category` 參數（篩選）兩種模式
- 可透過 `claude plugin install` 從本地 marketplace 安裝

**Non-Goals:**
- 不支援分頁或串流回傳
- 不快取 API 回應
- 不合併台北市與新北市資料

## Decisions

**延用 taipei-open-data-list 目錄結構**  
`plugins/new-taipei-open-data-list/commands/` 放 Flyte task，`skills/new-taipei-open-data-list/` 放 SKILL.md 與 pyproject.toml。與現有 Plugin 一致，降低維護成本。

**不設 SSL verify（`verify=False`）**  
新北市 API 同樣可能存在憑證問題（參考台北市 API 的已知問題），預設關閉 SSL 驗證，避免執行失敗。

**SKILL 觸發關鍵字使用「新北市」**  
SKILL.md description 包含「查詢新北市開放資料」、「列出新北市資料集」等，與台北市版本明確區隔，避免 Claude 混淆觸發來源。

## Risks / Trade-offs

- **API 欄位結構異動** → 新北市 API 若修改回傳欄位名稱，需同步更新 `parse_datasets()`；目前欄位名稱與台北市相同，風險低
- **SSL verify=False** → 有安全疑慮，但符合本專案現有慣例（台北市版本已採用）
- **無 API 認證** → 新北市 API 目前為公開無需認證，若未來加入 token 機制需另行調整
