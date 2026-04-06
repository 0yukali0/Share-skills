---
name: hello-world
description: This skill should be used when the user asks to "say hello", "print hello world", "run hello world", or wants a simple Python hello world example written and executed.
version: 1.0.0
---

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | No | 要打招呼的對象，預設 "world" |

# Hello World Skill

當使用者要求 hello world 示範時，依序執行以下步驟：

## 步驟 1 — 寫入 Python 程式

使用 Bash tool 執行：

```bash
uv sync --locked && source .venv/bin/activate && flyte run --local ../../commands/hello-world.py hello --name <name>
```

## 步驟 2 — 回報結果

告知使用者執行輸出，並說明示範完成。
