from math import ceil

import dash_core_components as dcc


def get_component(min_time, max_time, time_step):
    seconds = (max_time - min_time).total_seconds()
    steps = ceil(seconds / time_step)

    return dcc.Slider(
        id='time-slider',
        min=0,
        max=steps-1,
        value=0,
        step=1)
