## ADDED Requirements

### Requirement: 下載新北市開放資料集 JSON
系統 SHALL 從 `https://data.ntpc.gov.tw/api/datasets/info/json` 下載資料集目錄，解析每筆資料的「資料集名稱」與「主題分類」欄位。

#### Scenario: 成功下載並解析資料
- **WHEN** 呼叫指令且 API 正常回應
- **THEN** 系統解析 JSON，取得所有資料集的「資料集名稱」與「主題分類」

#### Scenario: API 無法連線
- **WHEN** API 請求失敗（連線逾時或 HTTP 錯誤）
- **THEN** 系統印出明確錯誤訊息並終止，不回傳部分結果

### Requirement: 依主題分類篩選資料集
系統 SHALL 接受可選的 `category` 參數；若提供，則只回傳「主題分類」符合該值的資料集名稱 `List[str]`。

#### Scenario: 提供有效主題分類
- **WHEN** 使用者提供 `category="交通"` 且資料集中存在此分類
- **THEN** 系統回傳所有「主題分類」為「交通」的「資料集名稱」清單

#### Scenario: 提供不存在的主題分類
- **WHEN** 使用者提供 `category="不存在分類"`
- **THEN** 系統回傳空 `List[str]` 並印出提示訊息

#### Scenario: 篩選前去除前後空白
- **WHEN** 使用者提供的 `category` 前後有多餘空白
- **THEN** 系統執行 `.strip()` 後再比對，正確回傳結果

### Requirement: 無主題輸入時回傳全部資料集
系統 SHALL 在未提供 `category` 參數（或空字串）時，回傳全部資料集名稱 `List[str]`。

#### Scenario: 未提供主題分類
- **WHEN** 使用者未傳入 `category` 參數
- **THEN** 系統回傳完整資料集名稱清單

#### Scenario: 傳入空字串主題
- **WHEN** 使用者傳入 `category=""`
- **THEN** 系統視同未提供主題，回傳全部資料集名稱清單

### Requirement: 以 flyte run --local 執行
系統 SHALL 透過 `flyte run --local` 執行 `new_taipei_open_data_list.py` 中以 `@env.task` 裝飾的函式，與 `taipei-open-data-list` 執行方式一致。

#### Scenario: SKILL.md 執行指令正確
- **WHEN** 依 SKILL.md 步驟在 `skills/new-taipei-open-data-list/` 目錄執行指令
- **THEN** 指令成功完成並印出資料集名稱清單

### Requirement: Plugin 可透過 marketplace 安裝
系統 SHALL 在 `plugins/.claude-plugin/marketplace.json` 中登錄此 Plugin，使其可透過 `claude plugin install new-taipei-open-data-list` 安裝。

#### Scenario: 成功安裝 Plugin
- **WHEN** 執行 `claude plugin install new-taipei-open-data-list`
- **THEN** Plugin 安裝成功，狀態顯示為 enabled
