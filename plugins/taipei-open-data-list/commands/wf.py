import asyncio
from typing import Any, Dict, List

import flyte

API_URLS: Dict[str, str] = {
    "taipei": "https://data.taipei/api/frontstage/tpeod/dataset.download?format=json",
    "new-taipei": "https://data.ntpc.gov.tw/api/datasets/info/json",
}

DESCRIPTIONS: List[str] = ["資料集名稱", "資料集描述", "資料說明"]

env = flyte.TaskEnvironment(
    name="taipei_open_data_list_env",
    image=(
        flyte.Image.from_debian_base(
            name="taipei", python_version=(3, 13)
        ).with_pip_packages("httpx", "asyncio")
    ),
)


@env.task
def datasets_metadata(url: str) -> List[dict]:
    import httpx

    try:
        # verify=False: taipei/NTPC APIs have certificate issues
        response = httpx.get(url, timeout=30, verify=False)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP 請求失敗：{e}")
        return []
    except Exception as e:
        print(f"下載資料集時發生錯誤：{e}")
        return []


def _first(val: Any) -> str:
    if isinstance(val, list):
        return val[0] if val else ""
    return val


@env.task
def parse_datasets(raw: List[Any], wanted: List[str]) -> List[Dict[str, Any]]:
    result = []
    for item in raw:
        entry = {field: v for field in wanted if (v := _first(item.get(field, "")))}
        if entry:
            result.append(entry)
    return result


@env.task
async def get_raws(urls: Dict[str, str]) -> list:
    collect: List[Any] = []
    for url in urls.values():
        collect.append(datasets_metadata.aio(url))
    return list(await asyncio.gather(*collect))


@env.task
async def get_descriptions(raws: list) -> List[List[Dict[str, Any]]]:
    collect = []
    for raw in raws:
        collect.append(parse_datasets.aio(raw, DESCRIPTIONS))
    return list(await asyncio.gather(*collect))


@env.task
async def describe_wf(urls: Dict[str, str] = API_URLS) -> List[List[Dict[str, Any]]]:
    raws = await get_raws(urls)
    return await get_descriptions(raws)


LINKS: Dict[str, List[str]] = {
    "taipei": ["資料存取網址"],
    "new-taipei": ["識別碼", "提供格式"],
}


def taipei_datalink(api_url: str) -> str:
    if api_url.startswith("http"):
        return api_url
    return f"https://data.taipei/{api_url}"


def new_taipei_datalink(info: Dict[str, str]) -> str:
    id = info.get("識別碼", "")
    format = info.get("提供格式", "").split("、")[0].strip()
    return f"https://data.ntpc.gov.tw/api/datasets/{id}/{format}".lower()


@env.task
def extract_links(raw: List[Any], city: str) -> Dict[str, str]:
    result = {}
    for item in raw:
        name = item.get("資料集名稱", "")
        if not name:
            continue
        if city == "taipei":
            api_url = item.get("資料存取網址", "")
            if api_url:
                result[name] = taipei_datalink(api_url)
        elif city == "new-taipei":
            result[name] = new_taipei_datalink(item)
    return result


@env.task
async def links_wf(urls: Dict[str, str] = API_URLS) -> Dict[str, str]:
    raws = await get_raws(urls)
    collect = []
    for city, raw in zip(urls.keys(), raws):
        collect.append(extract_links.aio(raw, city))
    all_links = list(await asyncio.gather(*collect))
    result = {}
    for links in all_links:
        result.update(links)
    return result


@env.task
async def keyword_links_wf(
    urls: Dict[str, str] = API_URLS, keyword: str = ""
) -> Dict[str, str]:
    all_links = await links_wf.aio(urls)
    kw = keyword.lower()
    return {name: link for name, link in all_links.items() if kw in name.lower()}
