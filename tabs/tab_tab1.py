import streamlit as st
from streamlit_echarts import st_echarts
from dashboard.plots.lines import stacked_area
from dashboard.tools.options import update_options_with_user_overrides
from dashboard.tools.options import update_options_with_defaults
import pandas as pd


def create(data, metadata, cfg):
    data = data["/TimeSeries/ScenTechNodeTime"]
    metadata = metadata["/TimeSeries/ScenTechNodeTime"]

    config = {"selector" : "Node", "stacker": "Technology", "xaxis": "TimeStamp", "value": "GeneratedElectricity"}

    st.markdown(
        f"## Electricity flows for each technology filtered by region and scenario\n"
    )

    navbar, plotarea = st.columns([0.2, 0.8])

    with navbar:
        scenario = st.selectbox(
            label=f"Select the Scenario",
            options = data.index.get_level_values("Scenario").unique().tolist()
        )

        select = st.selectbox(
            label=f"Select the {metadata[config['selector']]['label']}",
            options=data.index.get_level_values(config["selector"]).unique().tolist(),
        )

    with plotarea:
        data = data.query(f"Scenario == '{scenario}'")
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
