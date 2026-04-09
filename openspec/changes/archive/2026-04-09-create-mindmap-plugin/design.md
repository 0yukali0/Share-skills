## Context

專案使用 plugin 架構，每個 plugin 包含 `commands/`（Python 腳本，使用 flyte task）和 `skills/`（SKILL.md 描述觸發條件與使用流程）。現有範例為 `hello-world-plugin`。需新增一個 mindmap plugin，能從文字輸入產生 Mermaid mindmap 並轉為 PNG 圖片。

## Goals / Non-Goals

**Goals:**
- 提供 `gen_mindmap_mermaid` 函數，接收主題與結構化內容，回傳合法的 Mermaid mindmap 語法字串
- 提供 `mermaid_to_png` 函數，將 Mermaid 語法字串轉為 PNG 檔案
- 使用 pytest 撰寫完整的單元測試
- 提供 SKILL.md 讓 Claude 知道何時及如何呼叫此 plugin
- 在 marketplace.json 中註冊此 plugin

**Non-Goals:**
- 不支援 Mermaid 以外的圖表格式（如 PlantUML）
- 不提供互動式編輯心智圖的功能
- 不處理超大型心智圖的效能優化

## Decisions

### 1. 使用 Mermaid mindmap 語法作為中間表示

**選擇**: Mermaid mindmap 語法
**替代方案**: PlantUML mindmap、自定義 JSON 結構
**理由**: Mermaid 語法簡潔直觀，生態系成熟，且 `mmdc`（mermaid-cli）可直接轉為圖片。與專案中可能已有的 Mermaid 使用保持一致。

### 2. 使用 mmdc（mermaid-cli）進行 PNG 轉換

**選擇**: 透過 subprocess 呼叫 `mmdc` CLI
**替代方案**: 使用 Puppeteer + Mermaid JS 直接渲染、使用線上 API
**理由**: `mmdc` 是官方推薦的 CLI 工具，安裝簡單（npm），無需管理瀏覽器實例或網路依賴。

### 3. 函數設計為兩步驟分離

**選擇**: `gen_mindmap_mermaid` 與 `mermaid_to_png` 分開
**理由**: 職責分離，方便測試與重用。使用者可以只取得 Mermaid 語法而不一定需要圖片。

### 4. 遵循 flyte task 架構

**選擇**: 使用 `@env.task` decorator，與 hello-world-plugin 一致
**理由**: 保持專案慣例一致性，方便透過 `flyte run --local` 執行。

### 5. 測試策略

**選擇**: 使用 pytest，測試 Mermaid 語法生成的正確性以及 PNG 轉換流程
**理由**: pytest 是 Python 標準測試框架，與 pyproject.toml 整合簡單。

## Risks / Trade-offs

- **[mmdc 未安裝]** → 在 `mermaid_to_png` 中檢查 `mmdc` 是否可用，不可用時拋出明確錯誤訊息
- **[Mermaid 語法錯誤]** → `gen_mindmap_mermaid` 需確保輸出為合法語法，測試中驗證
- **[mmdc 需要 Chromium]** → `mmdc` 底層依賴 Puppeteer/Chromium，首次安裝可能較慢，但為一次性成本
