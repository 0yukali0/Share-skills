## ADDED Requirements

### Requirement: gen_mindmap_mermaid 產生合法 Mermaid mindmap 語法
系統 SHALL 提供 `gen_mindmap_mermaid` 函數，接收主題（topic）與內容結構（items），回傳合法的 Mermaid mindmap 語法字串。輸出 MUST 以 `mindmap` 關鍵字開頭，並包含正確的縮排層級結構。

#### Scenario: 基本主題與子項目
- **WHEN** 呼叫 `gen_mindmap_mermaid(topic="Python", items=["Syntax", "Data Types", "Functions"])`
- **THEN** 回傳的字串 MUST 以 `mindmap` 開頭，包含根節點 "Python"，且每個子項目作為第一層子節點

#### Scenario: 巢狀結構
- **WHEN** 呼叫 `gen_mindmap_mermaid` 並傳入包含巢狀 dict 的 items
- **THEN** 回傳的 Mermaid 語法 MUST 正確反映多層級縮排結構

#### Scenario: 空內容
- **WHEN** 呼叫 `gen_mindmap_mermaid(topic="Empty", items=[])`
- **THEN** 回傳的字串 MUST 僅包含根節點，無子節點

### Requirement: mermaid_to_png 將 Mermaid 語法轉為 PNG 圖片
系統 SHALL 提供 `mermaid_to_png` 函數，接收 Mermaid 語法字串與輸出路徑，產生 PNG 圖片檔案。

#### Scenario: 成功轉換為 PNG
- **WHEN** 呼叫 `mermaid_to_png(mermaid_code="mindmap\n  root\n    A\n    B", output_path="output.png")`
- **THEN** 系統 MUST 在指定路徑產生 PNG 檔案

#### Scenario: mmdc 未安裝時的錯誤處理
- **WHEN** 系統上未安裝 `mmdc` 且呼叫 `mermaid_to_png`
- **THEN** 系統 MUST 拋出明確的錯誤訊息，指示需要安裝 `@mermaid-js/mermaid-cli`

### Requirement: 使用 flyte task 架構包裝
`create_mindmap.py` 中的函數 MUST 使用 `@env.task` decorator 定義為 flyte task，使其可透過 `flyte run --local` 執行。

#### Scenario: 透過 flyte 執行完整流程
- **WHEN** 使用者執行 `flyte run --local create_mindmap.py create_mindmap --topic "ML" --items '["Supervised", "Unsupervised"]' --output_path "ml.png"`
- **THEN** 系統 MUST 產生對應的 PNG 心智圖檔案

### Requirement: pytest 單元測試
系統 MUST 提供 `test_create_mindmap.py`，使用 pytest 測試 `gen_mindmap_mermaid` 與 `mermaid_to_png` 的功能。

#### Scenario: 測試 Mermaid 語法生成正確性
- **WHEN** 執行 pytest 測試
- **THEN** MUST 驗證 `gen_mindmap_mermaid` 產出的字串為合法 Mermaid mindmap 語法

#### Scenario: 測試 PNG 檔案產生
- **WHEN** 執行 pytest 測試（mmdc 可用時）
- **THEN** MUST 驗證 `mermaid_to_png` 成功產生 PNG 檔案且檔案大小大於 0

### Requirement: SKILL.md 描述
plugin MUST 包含 `SKILL.md`，描述此 skill 的名稱、觸發條件、輸入參數與執行步驟。

#### Scenario: SKILL.md 格式正確
- **WHEN** 檢視 SKILL.md
- **THEN** MUST 包含 frontmatter（name, description, version）、輸入參數表格、執行步驟說明

### Requirement: marketplace.json 註冊
`.claude-plugin/marketplace.json` MUST 包含新 plugin 的註冊條目。

#### Scenario: marketplace.json 包含新 plugin
- **WHEN** 讀取 `marketplace.json`
- **THEN** plugins 陣列 MUST 包含 name 為 `create-mindmap-plugin` 的條目，含 description 與 source 欄位
