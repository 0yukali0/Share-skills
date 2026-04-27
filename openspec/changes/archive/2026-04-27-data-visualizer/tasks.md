## 1. Plugin 目錄結構建立

- [x] 1.1 建立 `plugins/data-visualizer/commands/` 目錄
- [x] 1.2 建立 `plugins/data-visualizer/skills/data-visualizer/` 目錄

## 2. 依賴管理

- [x] 2.1 建立 `plugins/data-visualizer/commands/pyproject.toml`，宣告 `gradio` 依賴（requires-python >=3.13）
- [x] 2.2 在 `plugins/data-visualizer/commands/` 執行 `uv lock` 生成 `uv.lock`

## 3. SKILL.md 撰寫

- [x] 3.1 建立 `plugins/data-visualizer/skills/data-visualizer/SKILL.md`，包含 frontmatter（name, description, version）
- [x] 3.2 撰寫步驟 1：從使用者獲取有效 links（List[str]），說明如何驗證 URL 可存取（HTTP 200），支援 CSV / JSON
- [x] 3.3 撰寫步驟 2：分析各 link 的欄位與資料型態，依規則選擇適合的圖表類型（折線圖、柱狀圖、散點圖、熱力圖、圓餅圖）
- [x] 3.4 撰寫步驟 3：說明使用 `gr.HTML` 建立視覺化，HTML 內嵌 Plotly CDN，不需額外 Python 圖表套件
- [x] 3.5 撰寫步驟 4：說明如何建立 Python 函數，將抓取的資料轉為 Plotly JavaScript 並放入 `gr.HTML` 的 value
- [x] 3.6 撰寫步驟 5：說明啟動 Gradio server（`demo.launch(server_port=7860)`），並透過 playwright-skill 開啟瀏覽器驗證圖表渲染、截圖存至 `/tmp/data-visualizer-verify.png`，驗證完成後關閉 server

## 4. Marketplace 註冊

- [x] 4.1 在 `plugins/.claude-plugin/marketplace.json` 新增 `data-visualizer` plugin 條目（name, description, skills 路徑）

## 5. 驗證

- [x] 5.1 在 `plugins/data-visualizer/commands/` 執行 `uv sync --locked` 確認依賴安裝成功
- [x] 5.2 手動依照 SKILL.md 步驟，使用一個公開 CSV URL 跑完完整流程，確認 Gradio 啟動並截圖成功
