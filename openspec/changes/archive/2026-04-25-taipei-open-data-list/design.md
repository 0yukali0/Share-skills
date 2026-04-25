## Context

專案已有 `create-mindmap-plugin` 作為 plugin 範本，架構為：
- `commands/<name>.py`：以 `flyte.TaskEnvironment` 裝飾的主要邏輯，可透過 `flyte run --local` 執行
- `skills/<name>/SKILL.md`：Claude 讀取的 Skill 說明，定義觸發條件與執行步驟
- `skills/<name>/pyproject.toml`：Python 依賴，透過 `uv sync` 安裝
- `plugins/.claude-plugin/marketplace.json`：plugin 登錄目錄

新 plugin `taipei-open-data-list` 沿用相同結構，核心邏輯是 HTTP 下載 + JSON 解析 + 字串篩選。

## Goals / Non-Goals

**Goals:**
- 以與 `create-mindmap-plugin` 一致的目錄結構建立 plugin
- 從台北市開放資料 API 下載並解析資料集清單
- 支援依「主題分類」篩選，回傳 `List[str]` 格式的資料集名稱
- 無主題輸入時回傳全部資料集名稱

**Non-Goals:**
- 快取或持久化 API 資料
- 支援多個主題同時篩選
- 回傳資料集詳細欄位（僅回傳名稱）
- GUI 或互動式選單

## Decisions

### HTTP 套件：使用 `httpx` 而非 `requests`
`httpx` 與 `requests` API 相似，但支援 async，且為現代 Python 專案首選。`create-mindmap-plugin` 未使用 HTTP 套件，故此為新依賴，選 `httpx` 以保持現代化。

### 執行入口：沿用 `flyte.TaskEnvironment` + `flyte run --local`
與 `create-mindmap-plugin` 的 `create_mindmap.py` 結構一致，透過 `@env.task` 裝飾器，Skill 透過 `flyte run --local` 呼叫，保持 plugin 架構統一。

### 篩選邏輯：大小寫不敏感的完整字串比對
主題分類為中文固定詞彙（如「交通」、「環境」），採完整字串比對即可；加入 `.strip()` 處理空白，避免輸入差異導致無結果。

### 資料欄位名稱：直接使用中文 key
API 回傳 JSON 的 key 為中文（「資料集名稱」、「主題分類」），直接使用，不額外映射，保持與原始資料結構一致。

## Risks / Trade-offs

- **API 可用性**：若台北市 API 暫時不可用，指令將失敗 → 回傳明確錯誤訊息提示使用者
- **API 欄位變動**：若「資料集名稱」或「主題分類」欄位名稱改變，解析將失敗 → 在 key 不存在時以 `.get()` 回傳空字串，並印出警告
- **資料量大**：資料集數量龐大時，全部回傳可能過長 → 屬於使用者決策，不在 plugin 內截斷

## Migration Plan

1. 建立 `plugins/taipei-open-data-list/` 目錄結構
2. 實作 `commands/taipei_open_data_list.py`
3. 建立 `skills/taipei-open-data-list/pyproject.toml`（含 `httpx`、`flyte` 依賴）
4. 建立 `skills/taipei-open-data-list/SKILL.md`
5. 更新 `plugins/.claude-plugin/marketplace.json`
6. 在 `skills/taipei-open-data-list/` 下執行 `uv sync` 驗證依賴

無 rollback 需求（新增 plugin，不影響現有功能）。

## Open Questions

- 無
