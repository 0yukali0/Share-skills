## Context

目前專案已有 `taipei-open-data-list` plugin 作為參考結構，使用 `flyte` + `uv` 管理依賴。`data-visualizer` plugin 新增視覺化能力，以 Gradio 作為前端框架，透過 `gr.HTML` 元件嵌入自訂圖表（Plotly / Chart.js）。Claude 扮演 orchestrator 角色，分析資料並生成視覺化程式碼，再透過 Playwright 驗證結果。

## Goals / Non-Goals

**Goals:**
- 提供 SKILL.md 讓 Claude 能按步驟完成「取得連結 → 分析欄位 → 選圖 → 生成 gr.HTML 視覺化 → Playwright 驗證」完整流程
- 使用 `pyproject.toml` + `uv.lock` 管理 `gradio` 依賴
- 結構與 `taipei-open-data-list` 一致（`commands/` 放 pyproject + uv.lock，`skills/` 放 SKILL.md）

**Non-Goals:**
- 不建立 flyte workflow（data-visualizer 的邏輯由 Claude 在 SKILL 步驟中直接生成 Python 程式碼執行，不需要 flyte）
- 不支援認證或 OAuth 的資料來源
- 不提供持久化儲存或資料庫

## Decisions

### 使用 gr.HTML 而非 gr.Plot
- **決定**：使用 `gr.HTML` 搭配 Plotly CDN 或 Chart.js 嵌入圖表 HTML 字串
- **原因**：`gr.HTML` 允許完全自訂的互動式圖表，不受 Gradio 內建圖表 API 限制；使用者提供的資料格式多樣，需要靈活的渲染層
- **替代方案**：`gr.Plot`（matplotlib）— 靜態圖，不支援互動；`gr.LinePlot` — 欄位限制多

### 依賴管理：gradio only
- **決定**：`pyproject.toml` 只宣告 `gradio`；圖表 library（Plotly/Chart.js）透過 CDN 在 HTML 內載入
- **原因**：減少 Python 依賴，避免版本衝突；Plotly CDN 在 gr.HTML 中直接可用

### 驗證：Playwright
- **決定**：啟動 Gradio server 後，用 `playwright` 截圖或檢查 DOM 確認圖表已渲染
- **原因**：SKILL.md 已規範使用 playwright-skill 驗證，與現有工具鏈一致

### Plugin 結構
```
plugins/data-visualizer/
  commands/
    pyproject.toml    # gradio 依賴
    uv.lock           # 鎖定版本
  skills/
    data-visualizer/
      SKILL.md        # Claude 執行步驟
```

## Risks / Trade-offs

- [外部連結格式多樣] → SKILL 步驟 3.1 明確要求驗證 URL 可存取（HTTP 200），並說明支援 CSV / JSON 兩種格式
- [圖表選型主觀] → SKILL 步驟 3.2 提供選型規則（時間序列→折線圖、類別分佈→柱狀圖、矩陣相關性→熱力圖）
- [Gradio port 衝突] → SKILL 步驟 3.5 指定 `server_port` 使用隨機 port 或 7860，並在 Playwright 驗證後關閉 server
