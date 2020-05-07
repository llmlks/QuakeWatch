import math

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np

from app import app
from components.config.timestep_picker import DEFAULT_TIMESTEP


def get_component():
    """Return the opacity toggler component."""

    return html.Div(children=[
        html.Div(
            dbc.Checklist(
                id='opacity-toggle',
                className='toggle-select',
                options=[{
                    'label': 'Show earthquakes cumulatively',
                    'value': 1
                }],
                value=[],
                switch=True
            ),
            title='Toggle showing all earthquakes cumulatively from the start'
            ' date until the end of the active time step'
        ),
        html.Div(id='opacity-config', className='hidden', children=[
            html.Div(
                className='config-label', children='Opacity decrease rate'),
            dbc.Input(
                id='opacity-value', type='number', min=1, step=1, value=1),
            dcc.Dropdown(
                id='opacity-unit',
                clearable=False,
                searchable=False,
                options=[
                    {'label': 'Seconds', 'value': 1},
                    {'label': 'Minutes', 'value': 60},
                    {'label': 'Hours', 'value': 60*60},
                    {'label': 'Days', 'value': 24*60*60},
                    {'label': 'Weeks', 'value': 7*24*60*60},
                    {'label': 'Months', 'value': 30*7*24*60*60}
                ],
                value=DEFAULT_TIMESTEP
            )
        ], title='Control the rate of the decrease of opacity, which decreases'
           + 'as a logarithmic function of time in the selected unit of time')
    ])


def get_opacities(dates, start_time=None, end_time=None,
                  timestep=DEFAULT_TIMESTEP, use_date=False):
    """Return an array containing an opacity for each row in the given Series.

    If the start time is None or use date is false, return an array of default
    values of 0.3. Else, compute the opacities with a log function with respect
    to the end time using the timestep to determine the rate of increase and
    scaling the results to range [0,1].

    Keyword arguments:
    dates -- Pandas Series of datetime objects
    start_time -- Datetime object representing the start time
    end_time -- Datetime object representing the end time
    timestep -- Integer representing the number of seconds used to scale time
        differences
    use_date -- A boolean indicating whether to use dates to compute opacities
    """

    if start_time is None or not use_date:
        return np.repeat(0.3, dates.shape[0])

    opacities = dates.apply(
        lambda x: math.log(max((end_time - x).total_seconds() / timestep, 1))
    )

    time_diff = max(
        1.1, (end_time - start_time).total_seconds() / timestep
    )

    return 1 - opacities.to_numpy() / math.log(time_diff)


@app.callback(
    Output('opacity-config', 'className'),
    [Input('opacity-toggle', 'value')])
def toggle_opacity_config_visibility(show_config):
    """Toggle the visible state of the opacity configuration based on whether
    the selected state of the opacity toggle.

    Keyword arguments:
    show_config -- An array with length of 1 if the toggle is on
    """
    if len(show_config) != 1:
        return 'hidden'
