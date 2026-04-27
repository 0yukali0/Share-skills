## Requirements

### Requirement: 依關鍵字過濾並回傳資料集連結
系統 SHALL 提供 `keyword_links_wf(urls, keyword)` task，從指定 API 來源取得所有資料集連結後，回傳資料集名稱包含關鍵字的子集，格式為 `Dict[str, str]`（資料集名稱→下載連結）。關鍵字比對 SHALL 不區分大小寫。

#### Scenario: 關鍵字有匹配結果
- **WHEN** 使用者呼叫 `keyword_links_wf` 並傳入存在於資料集名稱中的關鍵字
- **THEN** 回傳僅包含名稱含該關鍵字的資料集名稱與連結的 dict

#### Scenario: 關鍵字無匹配結果
- **WHEN** 使用者呼叫 `keyword_links_wf` 並傳入不存在於任何資料集名稱的關鍵字
- **THEN** 回傳空 dict

#### Scenario: 關鍵字大小寫不敏感
- **WHEN** 使用者傳入英文關鍵字（如 `json`）
- **THEN** 名稱含 `JSON`、`Json`、`json` 的資料集均被納入結果

### Requirement: SKILL.md 說明文件風格統一
SKILL.md SHALL 以統一的繁體中文行文、一致的表格與指令區塊格式呈現，並包含 `keyword_links_wf` 的使用說明（指令範例、參數說明、回傳格式）。

#### Scenario: 使用者查閱 keyword_links_wf 用法
- **WHEN** 使用者閱讀 SKILL.md 的連結查詢章節
- **THEN** 可找到 `keyword_links_wf` 的 flyte run 指令範例與參數說明
