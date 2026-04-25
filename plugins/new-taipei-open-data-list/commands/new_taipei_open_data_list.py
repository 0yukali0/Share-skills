import httpx
import flyte

API_URL = "https://data.ntpc.gov.tw/api/datasets/info/json"

env = flyte.TaskEnvironment(name="new_taipei_open_data_list_env")


def fetch_datasets() -> list[dict]:
    try:
        # verify=False: NTPC API may have certificate issues similar to Taipei city API
        response = httpx.get(API_URL, timeout=30, verify=False)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP 請求失敗：{e}")
        raise
    except Exception as e:
        print(f"下載資料集時發生錯誤：{e}")
        raise


def parse_datasets(raw: list[dict]) -> list[dict]:
    result = []
    for item in raw:
        name = item.get("資料集名稱", "")
        category = item.get("主題分類", "")
        if name:
            result.append({"資料集名稱": name, "主題分類": category})
    return result


@env.task
def new_taipei_open_data_list(category: str = "") -> list[str]:
    raw = fetch_datasets()
    datasets = parse_datasets(raw)

    category = category.strip()
    if category:
        filtered = [d["資料集名稱"] for d in datasets if d["主題分類"] == category]
        if not filtered:
            print(f"找不到主題分類「{category}」的資料集，請確認分類名稱是否正確。")
        return filtered
    else:
        return [d["資料集名稱"] for d in datasets]
