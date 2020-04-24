import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import histogram_column_picker
from components.config import date_picker


def get_component(columns, min_date, max_date, default_end_date):
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
        histogram_column_picker.get_component(columns),
        dbc.Button('Apply', id='apply', outline=True, color='success')
    ])
