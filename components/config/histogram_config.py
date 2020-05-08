import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import axis_picker
from components.config import date_picker


def get_component(columns, min_date, max_date, default_end_date,
                  default_column):
    """ Return the configuration component for the histogram view.

    Keyword arguments:
    columns -- The available columns in the uploaded data
    min_date -- The minimum date allowed to pick with the datepicker
    max_date -- The maximum date allowed to pick with the datepicker
    default_end_date -- The default end date for the datepicker. The
        default start date is the `min_date`.
    """

    return html.Div([
        date_picker.get_component(min_date, max_date, default_end_date),
        axis_picker.get_component(columns, default_column, is_histogram=True),
        html.Div([
            html.Div(
                className='config-label', children='Maximum number of bins'
            ),
            dbc.Input(id='nbins', type='number', min=2, step=1, value=10),
        ], title='Select the maximum number of bins used'),
        dbc.Button('Apply', id='apply', outline=True, color='success')
    ])
