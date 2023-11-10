import random
import pandas as pd


def heatmap(data, metadata):

    hours = [f"{i:0>2}" for i in range(24)]
    days = list(range(1, 365))
    col = data.name
    data = data.to_frame()
    data["_datetime"] = pd.to_datetime(data.index)

    df = data.groupby(
        [data["_datetime"].dt.dayofyear, data["_datetime"].dt.hour]
    )[col].sum()
    df.index.names = ["day", "hour"]
    lower_bound = df.min()
    upper_bound = df.max()
    df = df.reset_index()
    df["day"] = df["day"].astype(int)
    df["hour"] = df["hour"].astype(int)
    data = df.values.tolist()

    option = {
    "tooltip": {
        "position": 'top'
    },
    "grid": {
        "height": '75%',
        "top": '10%'
    },
    "yAxis": {
        "type": 'category',
        "data": hours,
        "name": "Hour of the day",
        "nameLocation": "middle",
        "nameGap": 50,
        "splitArea": {
        "show": True
        }
    },
    "xAxis": {
        "type": 'category',
        "data": days,
        "name": "Day of the year",
        "nameLocation": "middle",
        "nameGap": 25,
        "splitArea": {"show": True}
    },
    "visualMap": {
        "min": lower_bound,
        "max": upper_bound,
        "calculable": True,
        "orient": 'vertical',
        "top": 'center',
        "left": '90%'
    },
    "series": [
        {
        "name": metadata[col]["label"],
        "type": 'heatmap',
        "data": data,
        "label": {
            "show": False
        },
        "emphasis": {
            "itemStyle": {
            "shadowBlur": 10,
            "shadowColor": 'rgba(0, 0, 0, 0.5)'
            }
        }
        }
    ]
    }

    return option