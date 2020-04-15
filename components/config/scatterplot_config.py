import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import axis_picker
from components.config import color_picker
from components.config import size_picker
from components.config import date_picker


def get_component(min_date, max_date, default_end_date, columns,
                  numeric_columns, default_x, default_y, default_size):
    """Return the configuration component for the scatter plot view.

    Keyword arguments:
    min_date -- The minimum date allowed to pick with the datepicker.
    max_date -- The maximum date allowed to pick with the datepicker.
    default_end_date -- The default end date for the datepicker. The
        default start date is the `min_date`.
    columns -- The available columns in the uploaded data
    numeric_columns -- Available numeric columns
    default_x -- Column to use for x-axis by default
    default_y -- Column to use for y-axis by default
    default_size -- Column to use for sizes by default
    """
    return html.Div([
        date_picker.get_component(min_date, max_date, default_end_date),
        axis_picker.get_component(columns, default_x),
        axis_picker.get_component(columns, default_y, False),
        size_picker.get_component(numeric_columns, default_size),
        color_picker.get_component(numeric_columns),
        dbc.Button('Apply', id='apply', outline=True, color='success')
    ])
