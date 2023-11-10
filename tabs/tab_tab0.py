import streamlit as st
from streamlit_echarts import st_echarts
from dashboard.plots.barplots import barplot_grouped
from dashboard.tools.options import update_options_with_user_overrides
from dashboard.tools.options import update_options_with_defaults
import pandas as pd


def create(data, metadata, cfg):
    data = data["/Scalars/ScenTechNode"]
    metadata = metadata["/Scalars/ScenTechNode"]

    config = {"selector" : "Node", "grouper": "Scenario"}
    col = "ElectricalInstalledCapacities"
    select = st.selectbox(
        label=f"Select {config['selector']}",
        options=data.index.get_level_values(config["selector"]).unique().tolist(),
    )

    df = data.query(f"Node == '{select}'")[[col]].round()
    df.index = df.index.droplevel("Node")
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
