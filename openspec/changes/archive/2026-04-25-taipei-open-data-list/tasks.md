## 1. 建立 Plugin 目錄結構

- [x] 1.1 建立 `plugins/taipei-open-data-list/commands/` 目錄
- [x] 1.2 建立 `plugins/taipei-open-data-list/skills/taipei-open-data-list/` 目錄

## 2. 實作核心指令

- [x] 2.1 建立 `plugins/taipei-open-data-list/commands/taipei_open_data_list.py`，使用 `flyte.TaskEnvironment` 與 `@env.task` 裝飾器
- [x] 2.2 實作 HTTP 下載邏輯：以 `httpx` GET `https://data.taipei/api/frontstage/tpeod/dataset.download?format=json`，加入錯誤處理
- [x] 2.3 實作 JSON 解析邏輯：擷取每筆資料的「資料集名稱」與「主題分類」欄位（使用 `.get()` 防止 key 不存在）
- [x] 2.4 實作篩選邏輯：`category` 非空時過濾符合主題的資料集，空值時回傳全部；輸入執行 `.strip()` 後比對
- [x] 2.5 在檔案底部加入範例呼叫（無 category 與有 category 各一）

## 3. 設定 Python 依賴

- [x] 3.1 建立 `plugins/taipei-open-data-list/skills/taipei-open-data-list/pyproject.toml`，加入 `httpx` 與 `flyte>=2.0.9` 依賴
- [x] 3.2 在 `plugins/taipei-open-data-list/skills/taipei-open-data-list/` 目錄下執行 `uv sync` 產生 `uv.lock`

## 4. 建立 Skill 說明文件

- [x] 4.1 建立 `plugins/taipei-open-data-list/skills/taipei-open-data-list/SKILL.md`，定義觸發條件、輸入參數表格、執行步驟（`uv sync` → `flyte run --local`）

## 5. 更新 Marketplace 登錄

- [x] 5.1 在 `plugins/.claude-plugin/marketplace.json` 的 `plugins` 陣列新增 `taipei-open-data-list` 條目（name、description、source）

## 6. 驗證

- [x] 6.1 執行 SKILL.md 中的指令（不帶 category），確認回傳全部資料集名稱清單
- [x] 6.2 執行帶 category 參數的指令，確認只回傳指定主題的資料集
