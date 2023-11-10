from dashboard.tools import update_options_with_user_overrides


def _default_scatterplot_options():
    options = {
        'tooltip': {
            'position': 'top'
        },
        'yAxis': {
            'nameLocation': 'middle',
            'nameGap': 50,
        },
        'xAxis': {
            'nameLocation': 'middle',
            'nameGap': 50,
        }
    }
    return options


def scatterplot(data, metadata):
    options = {
        "xAxis": {},
        "yAxis": {},
        "series": {
            "symbolSize": 10,
            "data": data.tolist(),
            "type": "scatter",
        },
    }

    options = update_options_with_user_overrides(_default_scatterplot_options(), options)
    return options