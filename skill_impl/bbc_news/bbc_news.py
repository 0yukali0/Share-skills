from typing import List

import flyte

env = flyte.TaskEnvironment(name="bbc_news_env")
bbc_news_env = flyte.TaskEnvironment(
    name="bbc_news_env",
    image=flyte.Image.from_debian_base(python_version=(3, 13)).with_apt_packages(
        "requests>=2.32.5"
    ),
)

# 1️⃣ 取得 BBC News RSS 原始 XML
@bbc_news_env.task
def bbc_news(url: str = "https://feeds.bbci.co.uk/news/rss.xml") -> str:
    import requests
    response = requests.get(url)
    response.raise_for_status()  # 若請求失敗會丟例外
    return response.text  # 回傳 RSS XML 字串


# 2️⃣ 從 RSS XML 解析標題列表
@env.task
def news_titles(context: str) -> List[str]:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(context)
    titles = []
    # RSS 的新聞標題在 <item><title> 中
    for item in root.findall(".//item"):
        title_elem = item.find("title")
        if title_elem is not None and title_elem.text:
            titles.append(title_elem.text)
    return titles


@env.task
def bbc_news() -> str:
    news_xml = bbc_news()
    titles = news_titles(news_xml)
    res = "\n"
    for idx, title in enumerate(titles, start=1):
        res += f"{idx}. {title}\n"
    return res
