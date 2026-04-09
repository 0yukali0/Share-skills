## 1. Plugin 目錄結構建立

- [x] 1.1 建立 `plugins/create-mindmap-plugin/commands/` 與 `plugins/create-mindmap-plugin/skills/create-mindmap/` 目錄結構
- [x] 1.2 建立 `pyproject.toml`，加入 flyte、pytest 依賴，並執行 `uv sync`

## 2. 核心函數實作

- [x] 2.1 在 `commands/create_mindmap.py` 實作 `gen_mindmap_mermaid(topic, items)` 函數，產出合法 Mermaid mindmap 語法
- [x] 2.2 在 `commands/create_mindmap.py` 實作 `mermaid_to_png(mermaid_code, output_path)` 函數，透過 subprocess 呼叫 mmdc 轉換為 PNG
- [x] 2.3 使用 `@env.task` decorator 包裝主函數 `create_mindmap`，串接兩步驟並透過 flyte run 可執行

## 3. 測試

- [x] 3.1 建立 `commands/test_create_mindmap.py`，使用 pytest 測試 `gen_mindmap_mermaid` 語法正確性（基本、巢狀、空內容情境）
- [x] 3.2 測試 `mermaid_to_png` 成功產生 PNG 檔案（mmdc 可用時）及 mmdc 未安裝時的錯誤處理
- [x] 3.3 執行 pytest 確認所有測試通過

## 4. Skill 與 Marketplace 註冊

- [x] 4.1 撰寫 `skills/create-mindmap/SKILL.md`，包含 frontmatter、輸入參數表格、執行步驟
- [x] 4.2 更新 `plugins/.claude-plugin/marketplace.json`，新增 create-mindmap-plugin 條目
