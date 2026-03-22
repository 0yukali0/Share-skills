---
name: bbc_news
description: Fetch and display the latest news headlines from BBC News. Use when the user asks for BBC news, current headlines, or today's news.
license: Apache License 2.0
metadata:
  author: yuteng
  version: "1.0"
---

## Goals
Fetch and display the latest news headlines from BBC News RSS feed.

## Steps
1. Execute `flyte run --local skill_impl/bbc_news/bbc_news.py bbc_news > result.txt && cat result.txt` command.
2. Display the top 5 news titles from the output in a numbered list.

## Example Output
Latest BBC News headlines:
1. UK inflation rises to highest level in months
2. Scientists discover new treatment for common disease
3. Global leaders meet for climate summit
4. Tech giant announces major product launch
5. National team wins championship