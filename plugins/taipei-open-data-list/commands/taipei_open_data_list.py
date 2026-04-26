from typing import Dict, List, Any, Tuple
import asyncio
import flyte

API_URLS: Dict[str, str] = {
    "taipei": "https://data.taipei/api/frontstage/tpeod/dataset.download?format=json",
    "new-taipei": "https://data.ntpc.gov.tw/api/datasets/info/json",
}

env = flyte.TaskEnvironment(
    name="taipei_open_data_list_env",
    image = (
        flyte.Image.from_debian_base(
            name="my-image",
            python_version=(3, 13)
        )
        .with_pip_packages("httpx", "asyncio")
    )
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

@env.task
def parse_datasets(raw: List[Any]) -> List[Dict[str, Any]]:
    result = []
    for item in raw:
        name = item.get("資料集名稱", "")
        if name:
            result.append({"資料集名稱": name})
    return result


@env.task
async def taipei_open_data_list(urls: Dict[str, str] = API_URLS) -> List[List[Dict[str, Any]]]:
    collect: List[Any] = []
    for url in urls.values():
        collect.append(datasets_metadata.aio(url))
    all_raws = list(await asyncio.gather(*collect))
    collect = []
    for raw in all_raws:
        collect.append(parse_datasets.aio(raw))
    return list(await asyncio.gather(*collect))