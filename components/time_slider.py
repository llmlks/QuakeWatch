from math import ceil
import datetime

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app


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

    return html.Div([
        dbc.Button(
            id='time-slider-play-button',
            children=html.I(
                id='play-button-icon',
                className='fas fa-play'
            )
        ),
        dcc.Slider(
            id='time-slider',
            min=0,
            max=steps-1,
            value=0,
            step=1
        ),
        html.Div(
            [get_time_string(min_time, time_step)],
            id='time-slider-value-container'
        ),
        dcc.Interval(
            id='auto-stepper',
            interval=2000,
            n_intervals=None,
            disabled=True
        )
    ])


def get_time_string(time, timestep):
    """Return a string representation of the given datetime
    object with end time calculated using the timestep.

    Keyword arguments:
    time -- A datetime object to be converted into a string
    timestep -- The time step as seconds. One slider step represents
        a time window of this size.
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


@app.callback(
    Output('play-button-icon', 'className'),
    [Input('auto-stepper', 'disabled')])
def update_play_button(disabled):
    """Toggle the icon on the play/pause button.

    Keyword arguments:
    disabled -- Boolean indicating whether the interval is disabled
    """

    if disabled:
        return 'fas fa-play'

    return 'fas fa-pause'


@app.callback(
    Output('time-slider', 'value'),
    [Input('auto-stepper', 'n_intervals')],
    [State('time-slider', 'value'),
     State('time-slider', 'max')])
def update_slider_on_play(intervals, value, max_value):
    """Update time slider by adding one to its value.

    Keyword arguments:
    intervals -- Current number of intervals
    value -- Current value of the time slider
    max_value -- Maximum value of the time slider
    """
    if intervals is None:
        raise PreventUpdate

    return (value + 1) % (max_value + 1)


@app.callback(
    Output('auto-stepper', 'disabled'),
    [Input('time-slider-play-button', 'n_clicks')],
    [State('play-button-icon', 'className')])
def stop_and_start_interval(clicks, classname):
    """Start or stop the interval controlling automatic play
    of the time slider. The time slider is started/stopped
    based on the button's class name.

    Keyword arguments:
    clicks -- Number of clicks on the play/pause button
    classname -- Class name defining the icon shown on the button
    """
    if clicks is None:
        raise PreventUpdate

    if 'play' in classname:
        return False

    return True


@app.callback(
    Output('time-slider-play-button', 'n_clicks'),
    [Input('time-slider', 'value')],
    [State('time-slider', 'max'),
     State('auto-stepper', 'disabled')])
def update_play_button_clicks(value, max_value, disabled):
    """Trigger a 'click' on the play/pause button if the slider
    reaches its maximum value, while on play.

    Keyword arguments:
    value -- Current value of the time slider
    max_value -- Maximum value of the time slider
    disabled -- Boolean indicating whether the interval is disabled
    """
    if disabled:
        raise PreventUpdate

    if value == max_value:
        return 1
