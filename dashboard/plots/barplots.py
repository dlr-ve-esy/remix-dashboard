from dashboard.tools import update_options_with_defaults, update_options_with_user_overrides

def _default_barplot_options():
    options = {
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            }
        },
        'grid': {
            'top': '25%',
            'left': '5%',
            'right': '5%',
            'bottom': '25%',
            'containLabel': True
        },
        'xAxis': {
            'type': 'category',
            'axisLabel': {
                'show': True,
                # 'align': 'right',
                # 'position': 'bottom',
                # 'rotate': 90,
                # 'verticalAlign': 'middle',
                # 'verticalAlign': 'bottom',
                'verticalAlign': 'top',
                # 'padding': [90, 90, 90, 90],
                # 'margin': [9, 9, 9, 9]
            },
            'axisTick': {
                'show': False
            },
            'minorTick': {
                'show': True
            }
        },
        'yAxis': {
            'type': 'value',
            'nameLocation': 'middle',
            'nameGap': 50,
            # 'axisTicks': {
            #     'show': False
            # },
            # 'splitLine':{ 'show': False },
            # 'axisLine': { 'show': False },
            'axisTick': { 'show': True },
            'axisLabel': { 'show': False }
        }
    }
    return options


def _default_barplot_series_options():
    options = {
        'type': 'bar',
        'barGap': 0.1,
        'emphasis': {
            'focus': 'series'
        },
    }
    return options


def barplot_simple(data, metadata=None):
    x_col = data.columns[0]
    y_col = data.columns[1]

    x = list(data[x_col].astype(str))
    y = list(data[y_col])

    options = {
        'xAxis': {
            'data': x
        },
        'yAxis': {
            'type': 'value',
        },
        'series': [
            {
            'data': y,
            'type': 'bar'
            }
        ]
    }

    options = update_options_with_user_overrides(_default_barplot_options(), options)
    return options
    

def barplot_grouped(data, metadata=None):
    x_col = data.columns[0]
    y_col = data.columns[1]
    g_col = data.columns[2]

    x = list(data[x_col].astype(str).unique())

    series_list = list()
    groups = list(data[g_col].astype(str).unique())
    for selection, s in data.groupby(g_col):
        y = list(s[y_col])
        d = {
            'name': selection,
            'data': y
        }
        d.update(_default_barplot_series_options())
        series_list.append(d)
    
    options = {
        'legend': {
            'data': groups,
        },
        'xAxis': {
            'data': x,
        },
        'series': series_list
    }

    options = update_options_with_user_overrides(_default_barplot_options(), options)
    return options
    

def barplot_stacked(self, data, metadata=None):
    x_col = data.columns[0]
    y_col = data.columns[1]
    s_col = data.columns[2]

    series_list = list()
    x = list(data.astype(str)[x_col].unique())
    stacks = list(data[s_col].astype(str).unique())
    for selection, s in data.groupby(s_col):
        y = list(s[y_col])
        d = {
            'name': selection,
            'stack': 'total',
            'data': y
        }
        d.update(_default_barplot_series_options())
        series_list.append(d)
    
    options = {
        'legend': {
            'data': stacks
        },
        'xAxis': {
            'data': x
        },
        'series': series_list
    }
    
    options = update_options_with_user_overrides(_default_barplot_options(), options)
    return options
    

def barplot_grouped_stacked(data, metadata):
    x_col = data.columns[0]
    y_col = data.columns[1]
    g_col = data.columns[2]
    s_col = data.columns[3]

    x = list(data[x_col].astype(str).unique())
    stacks = list(data[s_col].astype(str).unique())
    series_list = list()
    for selection, s in data.groupby([g_col, s_col]):
        group_name = selection[0]
        stack_name = selection[1]
        y = list(s[y_col].astype(str))
        d = {
            'name': stack_name,
            'stack': f'{group_name}',
            'data': y
        }
        d.update(_default_barplot_series_options())
        series_list.append(d)
    
    options = {
        'legend': {
            'data': stacks
        },
        'xAxis': {
            'data': x
        },
        'series': series_list
    }

    options = update_options_with_user_overrides(_default_barplot_options(), options)
    return options





        