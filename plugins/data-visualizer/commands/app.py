import base64
import json
from collections import defaultdict

import gradio as gr
import httpx


def iframe_wrap(inner_html: str, height: int = 520) -> str:
    full = f"""<!DOCTYPE html>
<html><head>
  <meta charset="utf-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC&display=swap" rel="stylesheet">
  <style>body{{margin:0;font-family:'Noto Sans TC',sans-serif}}</style>
</head><body>{inner_html}</body></html>"""
    encoded = base64.b64encode(full.encode()).decode()
    return f'<iframe src="data:text/html;base64,{encoded}" width="100%" height="{height}px" frameborder="0" style="border:none;"></iframe>'


def fetch_json(url: str) -> list[dict]:
    r = httpx.get(url, timeout=30, follow_redirects=True, verify=False)
    raw = r.json()
    return raw if isinstance(raw, list) else raw.get("data", [raw])


# ── Tab 1：新北市老人福利機構（各區4種床位堆疊橫條圖）
def build_tab1() -> str:
    rows = fetch_json("https://data.ntpc.gov.tw/api/datasets/8f6ef217-935a-44aa-bda2-4e127420f025/json")
    bed_keys = ["bed_for_caring_quantity", "bed_for_nursing_quantity",
                "bed_for_longterm_quantity", "bed_for_azh_quantity"]
    bed_labels = ["養護床位", "護理床位", "長期照顧床位", "失智照顧床位"]

    town_beds: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    for row in rows:
        town = row.get("town", "未知")
        for i, k in enumerate(bed_keys):
            try:
                town_beds[town][i] += int(row.get(k, 0) or 0)
            except ValueError:
                pass

    towns = sorted(town_beds.keys())
    colors = ["#4C9BE8", "#F4845F", "#56B489", "#E8C84C"]
    traces = []
    for i, label in enumerate(bed_labels):
        vals = [town_beds[t][i] for t in towns]
        traces.append(
            f'{{"type":"bar","name":"{label}","x":{json.dumps(vals)},"y":{json.dumps(towns)},'
            f'"orientation":"h","marker":{{"color":"{colors[i]}"}}}}'
        )
    traces_js = "[" + ",".join(traces) + "]"

    inner = f"""
<div id="c1" style="width:100%;height:500px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
Plotly.newPlot('c1',{traces_js},{{
  title:"新北市老人福利機構各區床位數",
  barmode:"stack",
  font:{{family:"'Noto Sans TC',sans-serif"}},
  xaxis:{{title:"床位數"}},
  yaxis:{{title:"行政區",automargin:true}},
  legend:{{orientation:"h",y:-0.15}},
  margin:{{l:80,r:20,t:60,b:80}}
}});
</script>"""
    return iframe_wrap(inner, 580)


# ── Tab 2：新北市銀髮俱樂部各區分布（直條圖）
def build_tab2() -> str:
    rows = fetch_json("https://data.ntpc.gov.tw/api/datasets/f531a808-4aab-4e5e-93f0-c34f9ff97a78/json")
    count: dict[str, int] = defaultdict(int)
    for row in rows:
        count[row.get("town", "未知")] += 1

    towns = sorted(count.keys())
    vals = [count[t] for t in towns]

    trace = (
        f'{{"type":"bar","x":{json.dumps(towns)},"y":{json.dumps(vals)},'
        f'"marker":{{"color":"#56B489","line":{{"color":"#3a8a63","width":1}}}}}}'
    )
    inner = f"""
<div id="c2" style="width:100%;height:440px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
Plotly.newPlot('c2',[{trace}],{{
  title:"新北市銀髮俱樂部各區數量（共 {len(rows)} 處）",
  font:{{family:"'Noto Sans TC',sans-serif"}},
  xaxis:{{title:"行政區",tickangle:-35}},
  yaxis:{{title:"數量（處）"}},
  margin:{{l:50,r:20,t:60,b:100}}
}});
</script>"""
    return iframe_wrap(inner, 520)


# ── Tab 3：老人福利服務歷年統計（多折線圖）
def build_tab3() -> str:
    rows = fetch_json("https://data.ntpc.gov.tw/api/datasets/9f641102-f5bf-42c5-984c-c0f3e66be9f3/json")
    rows_sorted = sorted(rows, key=lambda r: int(r.get("itemvalue1", 0)))
    years = [r["itemvalue1"] for r in rows_sorted]

    series = {
        "居家服務人次(男)": "itemvalue2",
        "居家服務人次(女)": "itemvalue3",
        "養護型床位(男)":   "itemvalue4",
        "養護型床位(女)":   "itemvalue5",
        "護理之家(男)":     "itemvalue6",
        "護理之家(女)":     "itemvalue7",
        "日間照顧(男)":     "itemvalue8",
        "日間照顧(女)":     "itemvalue9",
    }
    colors = ["#4C9BE8", "#F4845F", "#56B489", "#E8C84C",
              "#A05CE8", "#E85CA0", "#5CE8D4", "#E8A85C"]
    traces = []
    for (label, key), color in zip(series.items(), colors):
        vals = []
        for r in rows_sorted:
            try:
                vals.append(int(str(r.get(key, 0)).replace(",", "")))
            except ValueError:
                vals.append(0)
        traces.append(
            f'{{"type":"scatter","mode":"lines+markers","name":"{label}",'
            f'"x":{json.dumps(years)},"y":{json.dumps(vals)},"line":{{"color":"{color}"}}}}'
        )
    traces_js = "[" + ",".join(traces) + "]"

    inner = f"""
<div id="c3" style="width:100%;height:500px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
Plotly.newPlot('c3',{traces_js},{{
  title:"新北市老人福利服務歷年統計（2007–2024）",
  font:{{family:"'Noto Sans TC',sans-serif"}},
  xaxis:{{title:"年度"}},
  yaxis:{{title:"人次／人數"}},
  legend:{{orientation:"h",y:-0.3}},
  margin:{{l:60,r:20,t:60,b:130}}
}});
</script>"""
    return iframe_wrap(inner, 640)


# ── Tab 4：銀髮健身俱樂部各區分布（圓餅圖）
def build_tab4() -> str:
    rows = fetch_json("https://data.ntpc.gov.tw/api/datasets/a9098780-7871-4a48-baf8-9484e0a690b0/json")
    count: dict[str, int] = defaultdict(int)
    for row in rows:
        count[row.get("town", "未知")] += 1

    labels = list(count.keys())
    vals = [count[k] for k in labels]

    trace = (
        f'{{"type":"pie","labels":{json.dumps(labels)},"values":{json.dumps(vals)},'
        f'"hole":0.35,"textinfo":"label+percent"}}'
    )
    inner = f"""
<div id="c4" style="width:100%;height:480px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
Plotly.newPlot('c4',[{trace}],{{
  title:"新北市銀髮健身俱樂部各區分布（共 {len(rows)} 處）",
  font:{{family:"'Noto Sans TC',sans-serif"}},
  margin:{{l:20,r:20,t:60,b:20}}
}});
</script>"""
    return iframe_wrap(inner, 540)


# ── Tab 5：長照特約單位服務類型量（橫條圖）
def build_tab5() -> str:
    rows = fetch_json("https://data.ntpc.gov.tw/api/datasets/3405c89e-87d6-48be-9bc4-6e9b59bedd30/json")
    row = rows[0] if rows else {}

    service_map = {
        "A類 居家服務":       "anumber_quantity",
        "BA類 日間照顧":      "banumber_quantity",
        "BB類 團體家屋":      "bbnumber_quantity",
        "BC類 小規模多機能":  "bcnumber",
        "C類 社區照顧":       "cnumber",
        "D類 家庭照顧者":     "dnumber",
        "E類 交通接送":       "enumber",
        "G類 喘息服務":       "gnumber",
    }
    labels = list(service_map.keys())
    vals = []
    for k in service_map.values():
        try:
            vals.append(int(row.get(k, 0) or 0))
        except ValueError:
            vals.append(0)

    year = row.get("year", "?")
    season = row.get("season", "?")
    total = row.get("total", "?")

    trace = (
        f'{{"type":"bar","x":{json.dumps(vals)},"y":{json.dumps(labels)},'
        f'"orientation":"h","marker":{{"color":"#A05CE8","line":{{"color":"#7a3ab8","width":1}}}}}}'
    )
    inner = f"""
<div id="c5" style="width:100%;height:460px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
Plotly.newPlot('c5',[{trace}],{{
  title:"新北市長照特約單位（{year}年第{season}季，合計{total}單位）",
  font:{{family:"'Noto Sans TC',sans-serif"}},
  xaxis:{{title:"特約單位數"}},
  yaxis:{{automargin:true}},
  margin:{{l:130,r:30,t:70,b:60}}
}});
</script>"""
    return iframe_wrap(inner, 520)


# ── Gradio 應用
with gr.Blocks(title="台北新北高齡化資料儀表板", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# 台北市・新北市 高齡化資料儀表板\n"
        "資料來源：[台北市開放資料](https://data.taipei) ／ [新北市開放資料](https://data.ntpc.gov.tw)"
    )

    with gr.Tabs():
        with gr.Tab("老人福利機構床位"):
            gr.Markdown("**新北市老人福利機構** — 各行政區養護、護理、長期照顧、失智照顧床位數量")
            chart1 = gr.HTML()
        with gr.Tab("銀髮俱樂部分布"):
            gr.Markdown("**新北市銀髮俱樂部** — 各行政區俱樂部數量分布")
            chart2 = gr.HTML()
        with gr.Tab("老人福利服務趨勢"):
            gr.Markdown("**新北市老人福利服務歷年統計** — 居家服務、床位、日間照顧等 2007～2024 年趨勢")
            chart3 = gr.HTML()
        with gr.Tab("銀髮健身俱樂部"):
            gr.Markdown("**新北市銀髮健身俱樂部** — 各行政區分布圓餅圖")
            chart4 = gr.HTML()
        with gr.Tab("長照特約單位"):
            gr.Markdown("**新北市政府長照特約單位** — 各服務類型特約單位數量")
            chart5 = gr.HTML()

    def load_all():
        return build_tab1(), build_tab2(), build_tab3(), build_tab4(), build_tab5()

    demo.load(fn=load_all, outputs=[chart1, chart2, chart3, chart4, chart5])

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)
