## 1. Plugin 目錄結構建立

- [x] 1.1 建立 `plugins/new-taipei-open-data-list/commands/` 目錄
- [x] 1.2 建立 `plugins/new-taipei-open-data-list/skills/new-taipei-open-data-list/` 目錄

## 2. Flyte Task 實作

- [x] 2.1 建立 `plugins/new-taipei-open-data-list/commands/new_taipei_open_data_list.py`，實作 `fetch_datasets()`、`parse_datasets()`、`new_taipei_open_data_list()` Flyte task
- [x] 2.2 確認 API URL 為 `https://data.ntpc.gov.tw/api/datasets/info/json`，使用 `verify=False`
- [x] 2.3 確認 `category` 參數為可選，空字串時回傳全部資料集
- [x] 2.4 確認找不到分類時印出提示訊息並回傳空 list

## 3. Python 環境設定

- [x] 3.1 建立 `plugins/new-taipei-open-data-list/skills/new-taipei-open-data-list/pyproject.toml`（依賴 `flyte>=2.0.9`、`httpx>=0.27.0`，Python >=3.13）
- [x] 3.2 在 skill 目錄執行 `uv sync` 產生 `uv.lock`

## 4. SKILL.md 建立

- [x] 4.1 建立 `plugins/new-taipei-open-data-list/skills/new-taipei-open-data-list/SKILL.md`
- [x] 4.2 設定 description 觸發關鍵字（「查詢新北市開放資料」、「列出新北市資料集」等）
- [x] 4.3 確認執行指令路徑指向 `../../commands/new_taipei_open_data_list.py`

## 5. Marketplace 登錄

- [x] 5.1 在 `plugins/.claude-plugin/marketplace.json` 新增 `new-taipei-open-data-list` plugin 項目

## 6. 驗證

- [x] 6.1 執行 `claude plugin marketplace add` 並確認 marketplace 驗證通過
- [x] 6.2 執行 `claude plugin install new-taipei-open-data-list` 並確認安裝成功
- [x] 6.3 在 skill 目錄執行 `uv sync --locked && flyte run --local` 確認查詢全部資料集成功
- [x] 6.4 執行帶 `--category` 參數的指令確認篩選功能正常
