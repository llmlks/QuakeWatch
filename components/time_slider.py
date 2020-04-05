from math import ceil
import datetime

import dash_core_components as dcc
import dash_html_components as html


def get_component(min_time, max_time, time_step, visible=True):
    """Return the time slider component.

    The number of steps is calculated based on the argument values.

    Keyword arguments:
    min_time -- A datetime object representing the start of the time frame
    max_time -- A datetime object representing the end of the time frame
    time_step -- The time step as seconds. One slider step represents
        a time window of this size.
    visible -- A boolean indicating whether the component should be visible
    """
    seconds = (max_time - min_time).total_seconds()
    steps = ceil(seconds / time_step)

    display_style = {}
    if not visible:
        display_style = {'display': 'none'}

    return html.Div([
        dcc.Slider(
            id='time-slider',
            min=0,
            max=steps-1,
            value=0,
            step=1),
        html.Div(
            [get_time_string(min_time, time_step)],
            id='output-container-range-slider'
        )
    ], style=display_style)


def get_time_string(time, timestep):
    """Return a string representation of the given datetime
    object with end time calculated using the timestep.

    Keyword arguments:
    time -- A datetime object to be converted into a string
    timestep -- Unit of the timestep in seconds
    """
    end_time = time + datetime.timedelta(seconds=timestep)
    return '{}.{}.{} {}:{}:{} - {}.{}.{} {}:{}:{}'.format(
        str(time.day).zfill(2),
        str(time.month).zfill(2),
        time.year,
        str(time.hour).zfill(2),
        str(time.minute).zfill(2),
        str(time.second).zfill(2),
        str(end_time.day).zfill(2),
        str(end_time.month).zfill(2),
        end_time.year,
        str(end_time.hour).zfill(2),
        str(end_time.minute).zfill(2),
        str(end_time.second).zfill(2)
    )
