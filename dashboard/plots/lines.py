import pandas as pd

from dashboard.tools import update_options_with_user_overrides


def _default_line_options():
    return {
        "title": {"text": None},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"animation": False},
        },
        "axisPointer": {
            "link": [
                {"xAxisIndex": "all"}
            ]
        },
        "dataZoom": [
            {
                "type": 'slider',
                "start": 0,
                "end": 1,
                "xAxisIndex": 0,
                "zoomLock": True
            }
        ],
    }


def line(data, metadata):
    if not isinstance(data, pd.Series):
        msg = "Line function takes a series only!"
        raise TypeError(msg)

    label = metadata[data.name]["label"]
    unit = metadata[data.name]["unit"]
    options = {
        "legend": {"data": [metadata[data.name]["label"]]},
        "xAxis": {
            "type": "category",
            "data": data.index.tolist(),
        },
        "yAxis": {
            "type": "value",
            "name": f"{label} in {unit}",
            "nameLocation": "middle",
            "nameGap": 75
        },
        "series": [{
                "data": data.tolist(),
                "type": "line",
                "name": metadata[data.name]["label"]
            }
        ],
    }
    return update_options_with_user_overrides(_default_line_options(), options)


def  multiline(data, metadata):
    options = {
        "legend": {"data": [metadata[col]["label"] for col in metadata]},
        "xAxis": {
            "type": "category",
            "data": data.index.tolist(),
        },
        "yAxis": {"type": "value"},
        "series": [
            {"data": data[col].tolist(), "type": "line", "name": metadata[col]["label"]}
            for col in data.columns
        ],
    }
    return update_options_with_user_overrides(_default_line_options(), options)


def twolinetwoyaxes(data, metadata, axesmapping):
    options = {
        "legend": {"data": [metadata[col]["label"] for col in axesmapping]},
        "dataZoom": [
            {
                "show": True,
                "realtime": True,
                "start": 1,
                "end": 2,
                "xAxisIndex": [0, 1]
            },
            {
                "type": 'inside',
                "realtime": True,
                "start": 1,
                "end": 2,
                "xAxisIndex": [0, 1]
            }
        ],
        "grid": [
            {
                "left": 150,
                "right": 50,
                "height": '35%'
            },
            {
                "left": 150,
                "right": 50,
                "top": '50%',
                "height": '35%'
            }
        ],
        "xAxis": [
            {
                "type": 'category',
                "gridIndex": axisindex,
                "boundaryGap": False,
                "axisLine": { "onZero": True },
                "axisTick": { "show": False } if axisindex == 0 else {},
                "axisLabel": { "show": False } if axisindex == 0 else {},
                "data": data.index.tolist()
            } for axisindex in axesmapping.values()
        ],
        "yAxis": [
            {
                "gridIndex": axisindex,
                "name": f'{metadata[col]["label"]} in {metadata[col]["unit"]}',
                "nameLocation": "middle",
                "nameGap": 75,
                "type": 'value',
            } for col, axisindex in axesmapping.items()
        ],
        "series": [
            {
            "name": metadata[col]["label"],
            "type": 'line',
            "symbolSize": 8,
            "xAxisIndex": axesmapping[col],
            "yAxisIndex": axesmapping[col],
            "data": data[col].tolist()
            } for col in axesmapping
        ]
    }
    return update_options_with_user_overrides(_default_line_options(), options)


def twolinestwoyaxesonesubplot(data, metadata, axesmapping):
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
            "type": 'cross',
            "crossStyle": {
                "color": '#999'
            }
            }
        },
        "toolbox": {
            "feature": {
            "dataView": { "show": True, "readOnly": False },
            "magicType": { "show": True, "type": ['line', 'bar'] },
            "restore": { "show": True },
            "saveAsImage": { "show": True }
            }
        },
        "legend": {"data": [metadata[col]["label"] for col in axesmapping]},
        "xAxis": [
            {
            "type": 'category',
            "data": data.index.tolist(),
            }
        ],
        "yAxis": [
            {
            "type": 'value',
            "name": f'{metadata[col]["label"]} in {metadata[col]["unit"]}',
            "nameLocation": "middle",
            "nameGap": 75,
            "alignTicks": True
            } for col in axesmapping
        ],
        "series": [
            {
            "name": metadata[col]["label"],
            "type": 'line',
            "yAxisIndex": axisindex,
            "data": data[col].tolist()
            } for col, axisindex in axesmapping.items()
        ]
    }
    return update_options_with_user_overrides(_default_line_options(), option)


def stacked_area(data, metadata):
    datazoom = {
    "dataZoom": [
        {
            "type": 'slider',
            "start": 5,
            "end": 7,
            "xAxisIndex": 0,
            "zoomLock": True
        }
    ]
    }
    options = {
        "title": {"text": ""},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"animation": False},
        },
        "legend": {"data": [col for col in data.columns]},
        "toolbox": {"feature": {
            "dataZoom": {
                "yAxisIndex": 'none'
            },
            "restore": {},
            "saveAsImage": {}
        }},
        "axisPointer": {
        "link": [
            {
            "xAxisIndex": 'all'
            }
        ]
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
        "xAxis": [
            {
                "type": "category",
                "boundaryGap": True,
                "axisLine": {"onZero": True},
                "data": data.index.tolist(),
            }
        ],
        "yAxis": [{"type": "value"}],
        "series": [
            {
                "data": data[col].tolist(),
                "type": "line",
                "name": col,
                "stack": "stack0",
                "areaStyle": {},
                "emphasis": {"focus": "series"}
            }
            for col in data.columns
        ],
    }
    options["dataZoom"] = datazoom["dataZoom"]
    return options
