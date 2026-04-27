## Context

`wf.py` 已有 `links_wf` 回傳全部資料集的 `Dict[str, str]`（名稱→連結），以及 `extract_links` 負責單城市的連結產生邏輯。新的 `keyword_links_wf` 只需在 `links_wf` 的結果上加一層關鍵字過濾，無需改動現有 task。

## Goals / Non-Goals

**Goals:**
- 新增 `keyword_links_wf(urls, keyword)` task，回傳名稱含關鍵字的資料集連結
- 關鍵字比對不區分大小寫
- 更新 SKILL.md，風格統一並加入新 task 說明

**Non-Goals:**
- 不支援正規表達式或多關鍵字搜尋
- 不修改 `links_wf` 或 `extract_links` 現有介面
- 不做欄位內容（描述、格式）的關鍵字比對，僅比對資料集名稱

## Decisions

**複用 `links_wf` 而非重新實作**：`keyword_links_wf` 內部呼叫 `links_wf.aio()` 取得全量結果後過濾，避免重複 API 呼叫邏輯與 datalink 函式的維護負擔。

**過濾位置在 task 層而非 `extract_links`**：關鍵字過濾屬於查詢語義，不屬於連結產生邏輯，分開可保持各 task 職責單一。

## Risks / Trade-offs

- **效能**：每次呼叫仍需下載全量資料集清單再過濾，資料量大時較慢 → 目前資料量可接受，未來可加快取
- **名稱比對限制**：僅比對 `資料集名稱`，若關鍵字只出現在描述欄位則不會命中 → 符合當前需求範圍
