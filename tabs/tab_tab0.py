import streamlit as st
from streamlit_echarts import st_echarts
from dashboard.plots.barplots import barplot_grouped
from dashboard.tools.options import update_options_with_user_overrides
from dashboard.tools.options import update_options_with_defaults
import pandas as pd


def _grouped_bars(data, metadata, col):

    config = {"selector" : "Node", "grouper": "Scenario"}
    select = st.selectbox(
        label=f"Select {config['selector']}",
        options=data.index.get_level_values(config["selector"]).unique().tolist(),
        key=col
    )

    df = data.query(f"Node == '{select}'")[[col]].round()
    df.index = df.index.droplevel("Node")

    df = df[df.groupby('Technology')[col].transform(lambda x: (x != 0).any())]
    df.reset_index(inplace=True)

    bar_options = barplot_grouped(
        df[["Scenario", col, "Technology"]],
        metadata
    )
    bar_options = update_options_with_defaults(bar_options)

    options_update = {
        'yAxis': {
            'name': f'{metadata[col]["label"]} in {metadata[col]["unit"]}'
        }
    }
    bar_options = update_options_with_user_overrides(bar_options, options_update)
    st_echarts(bar_options, height="500px", width="95%")


def find_key_by_name(nested_dict, target_name):
    for key, nested_info in nested_dict.items():
        if nested_info.get('label') == target_name:
            return key
    return None  # Return None if the name is not found in any nested dictionary


def create(data, metadata, cfg):
    data = data["/Scalars/ScenTechNode"]
    metadata = metadata["/Scalars/ScenTechNode"]

    st.markdown(f"## Results grouped by scenario and filtered by country")

    col = st.selectbox(
        "Select the indicator",
        options=[metadata[key]["label"] for key in data.columns]
    )
    col = find_key_by_name(metadata, col)
    _grouped_bars(data, metadata, col)
