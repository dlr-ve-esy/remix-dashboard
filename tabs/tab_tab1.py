import streamlit as st
from streamlit_echarts import st_echarts
from dashboard.plots.lines import stacked_area
from dashboard.tools.options import update_options_with_user_overrides
from dashboard.tools.options import update_options_with_defaults
import pandas as pd


def create(data, metadata, cfg):
    data = data["/TimeSeries/ScenTechNodeTime"].query("Scenario == '3a'")
    metadata = metadata["/TimeSeries/ScenTechNodeTime"]

    config = {"selector" : "Node", "stacker": "Technology", "xaxis": "TimeStamp", "value": "GeneratedElectricity"}
    select = st.selectbox(
        label=f"Select {config['selector']}",
        options=data.index.get_level_values(config["selector"]).unique().tolist(),
    )

    df = pd.pivot_table(
        data.xs(select, level=config["selector"]),
        columns=config["stacker"],
        index=config["xaxis"],
        values=config["value"]
    ).dropna(how="any", axis=0)

    plotoptions = {
        "yAxis": [{
            "name": f'{metadata[config["value"]]["label"]} in {metadata[config["value"]]["unit"]}',
            "nameLocation": "middle",
            "nameGap": 50
        }]
    }

    line_options = stacked_area(
        df,
        metadata
    )
    line_options = update_options_with_defaults(line_options)
    line_options = update_options_with_user_overrides(line_options, plotoptions)
    st_echarts(line_options)
