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
    select = st.selectbox(
        label=f"Select {config['selector']}",
        options=data.index.get_level_values(config["selector"]).unique().tolist(),
    )

    df = data.query(f"Node == '{select}'")
    df.index = df.index.droplevel("Node")
    df.reset_index(inplace=True)
    bar_options = barplot_grouped(
        df[["Scenario", "ElectricalInstalledCapacities", "Technology"]],
        metadata
    )
    bar_options = update_options_with_defaults(bar_options)
    # line_options = update_options_with_user_overrides(line_options, plotoptions)
    st_echarts(bar_options)
