import streamlit as st
from streamlit_echarts import st_echarts, JsCode, Map
import json
from dashboard.plots.barplots import barplot_grouped
from dashboard.tools.options import update_options_with_user_overrides
from dashboard.tools.options import update_options_with_defaults


def _create_background_map():

    formatter = JsCode(
        "function (params) {"
        + "var value = (params.value + '').split('.');"
        + "value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');"
        + "return params.seriesName + '<br/>' + params.name + ': ' + value;}"
    ).js_code

    with open("./data/flexmex.geojson", "r", encoding="utf-8") as f:
        map = Map(
            "Europe",
            json.loads(f.read())
        )

    map_options = {
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
            "formatter": formatter,
        },
        "visualMap": {
            "left": "right",
            "top": "middle",
            "min": 500000,
            "max": 38000000,
            "inRange": {
                "color": [
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ]
            },
            "text": ["High", "Low"],
            "calculable": True,
        },
        "toolbox": {
            "show": True,
            "left": "left",
            "top": "top",
            "feature": {
                "dataView": {"readOnly": False},
                "restore": {},
                "saveAsImage": {},
            },
        }
    }
    return map_options, map


def find_key_by_name(nested_dict, target_name):
    for key, nested_info in nested_dict.items():
        if nested_info.get('label') == target_name:
            return key
    return None  # Return None if the name is not found in any nested dictionary


def create(data, metadata, cfg):

    data = data["/Scalars/ScenTechNode"]
    metadata = metadata["/Scalars/ScenTechNode"]

    config = {"selector" : "Technology", "grouper": "Scenario"}

    st.markdown(
        "On this map you can explore different indicators in the spatial "
        "resolution of the model. You can select the scenario, the commodity "
        "or installed capacity and the technology."
    )

    navbar, plotarea = st.columns([0.2, 0.8])

    with navbar:
        scen = st.selectbox(
            label=f"Select the {config['grouper']}",
            options=data.index.get_level_values(config["grouper"]).unique().tolist()
        )

        df = data.query(f"{config['grouper']} == '{scen}'")
        df.index = df.index.droplevel(config["grouper"])

        datacol = st.selectbox(
            label=f"Select the map information",
            options=[metadata[key]["label"] for key in data.columns]
        )
        col = find_key_by_name(metadata, datacol)

        df = df[[col]].round()
        df = df[df.groupby(config["selector"])[col].transform(lambda x: (x != 0).any())]

        select = st.selectbox(
            label=f"Select {config['selector']}",
            options=df.index.get_level_values(config["selector"]).unique().tolist(),
        )

    with plotarea:

        st.markdown(f"### {datacol}: {config['selector']} \"{select}\" in {metadata[col]['unit']}")

        df = df.query(f"{config['selector']} == '{select}'")[[col]].round()
        df.index = df.index.droplevel(config["selector"])

        nodelookup = {
            "AT": "Austria",
            "BE": "Belgium",
            "CH": "Switzerland",
            "CZ": "Czechia",
            "DE": "Germany",
            "DK": "Denmark",
            "FR": "France",
            "IT": "Italy",
            "LU": "Luxembourg",
            "NL": "Netherlands",
            "PL": "Poland"
        }

        map_options, map = _create_background_map()

        options = {
            "series": [
                {
                    "name": metadata[col]["label"],
                    "type": "map",
                    "roam": True,
                    "map": "Europe",
                    "emphasis": {"label": {"show": True}},
                    "data": [
                        {"name": nodelookup[node], "value": df.loc[node, col]} for node in df.index
                    ],
                }
            ],
            "visualMap": {
                "min": int(df.min().iloc[0]),
                "max": int(df.max().iloc[0])
            }
        }
        map_options = update_options_with_user_overrides(map_options, options)

        st_echarts(options, map=map, height="600px", width="75%")
