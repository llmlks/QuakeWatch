import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import axis_picker
from components.config import color_picker
from components.config import size_picker
from components.config import date_picker


def get_component(min_date, max_date, columns,
                  default_x, default_y, nbins_x, nbins_y):
    """Return the configuration component for the scatter plot view.

    Keyword arguments:
    min_date -- The minimum date allowed to pick with the datepicker.
    max_date -- The maximum date allowed to pick with the datepicker.
    columns -- The available columns in the uploaded data
    default_x -- Column to use for x-axis by default
    default_y -- Column to use for y-axis by default
    """
    return html.Div([
        date_picker.get_component(min_date, max_date, max_date),
        axis_picker.get_component(columns, default_x),
        axis_picker.get_component(columns, default_y, False),
        html.Div([
            html.Div(
                className='config-label', children='Number of bins for x'
            ),
            dbc.Input(id='nbins-x', type='number', min=1, step=1, value=40),
        ], title='Select the number of bins used for x'),
        html.Div([
            html.Div(
                className='config-label', children='Number of bins for y'
            ),
            dbc.Input(id='nbins-y', type='number', min=1, step=1, value=40),
        ], title='Select the number of bins used for y'),
        dbc.Button('Apply', id='apply', outline=True, color='success')
    ])
