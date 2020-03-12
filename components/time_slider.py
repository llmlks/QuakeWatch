from math import ceil

import dash_core_components as dcc


def get_component(min_time, max_time, time_step):
    """Return the time slider component.

    The number of steps is calculated based on the argument values.

    Keyword arguments:
    min_time -- A datetime object representing the start of the time frame
    max_time -- A datetime object representing the end of the time frame
    time_step -- The time step as seconds. One slider step represents
        a time window of this size.
    """
    seconds = (max_time - min_time).total_seconds()
    steps = ceil(seconds / time_step)

    return dcc.Slider(
        id='time-slider',
        min=0,
        max=steps-1,
        value=0,
        step=1)
