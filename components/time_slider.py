from math import ceil
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app


def get_component(min_time, max_time, time_step, interval_seconds=2):
    """Return the time slider component.

    The number of steps is calculated based on the argument values.

    Keyword arguments:
    min_time -- A datetime object representing the start of the time frame
    max_time -- A datetime object representing the end of the time frame
    time_step -- The time step as seconds. One slider step represents
        a time window of this size.
    interval_seconds -- The update frequency of the time slider in seconds
    """
    seconds = (max_time - min_time).total_seconds()
    steps = ceil(seconds / time_step)
    if interval_seconds is None:
        interval_seconds = 2

    return html.Div([
        html.Div(
            className='time-slider-button-group',
            children=[
                html.Div(
                    dbc.Button(
                        id='time-slider-backward-button',
                        children=html.I(
                            id='backward-button-icon',
                            className='fas fa-step-backward'
                        )
                    ),
                    className='slider-button',
                    title='Moves the slider one step backward'
                ),
                html.Div(
                    dbc.Button(
                        id='time-slider-play-button',
                        children=html.I(
                            id='play-button-icon',
                            className='fas fa-play'
                        )
                    ),
                    className='slider-button',
                    title='Moves the slider one step at a time until the end'
                    ' of the time range',
                    id='play-button'
                ),
                html.Div(
                    dbc.Button(
                        id='time-slider-forward-button',
                        children=html.I(
                            id='forward-button-icon',
                            className='fas fa-step-forward'
                        )
                    ),
                    className='slider-button',
                    title='Moves the slider one step forward'
                )
            ]
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
            interval=interval_seconds*1000,
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
    [Output('play-button-icon', 'className'),
     Output('play-button', 'title')],
    [Input('auto-stepper', 'disabled')])
def update_play_button(disabled):
    """Toggle the icon on the play/pause button.

    Keyword arguments:
    disabled -- Boolean indicating whether the interval is disabled
    """

    if disabled:
        return [
            'fas fa-play',
            'Moves the slider one step at a time until the end'
            ' of the time range. Updates every three seconds'
        ]

    return ['fas fa-pause', 'Pause the automatic update of the slider']


@app.callback(
    Output('time-slider', 'value'),
    [Input('auto-stepper', 'n_intervals'),
     Input('time-slider-forward-button', 'n_clicks'),
     Input('time-slider-backward-button', 'n_clicks')],
    [State('time-slider', 'value'),
     State('time-slider', 'max')])
def update_slider_on_play(intervals, forward, backward, value, max_value):
    """Update time slider by adding one to its value.

    Keyword arguments:
    intervals -- Current number of intervals
    forward -- Number of clicks on the forward button
    backward -- Number of clicks on the backward button
    value -- Current value of the time slider
    max_value -- Maximum value of the time slider
    """
    context = dash.callback_context

    if context.triggered:
        triggered_id = context.triggered[0]['prop_id'].split('.')[0]

        if triggered_id in ['auto-stepper', 'time-slider-forward-button']:
            return (value + 1) % (max_value + 1)

        if triggered_id == 'time-slider-backward-button':
            return (value - 1) % (max_value + 1)

    raise PreventUpdate


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
