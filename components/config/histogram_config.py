import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import histogram_column_picker
from components.config import date_picker


def get_component(columns, min_date, max_date, default_end_date):

    return html.Div([
        date_picker.get_component(min_date, max_date, default_end_date),
        histogram_column_picker.get_component(columns),
        dbc.Button('Apply', id='apply', outline=True, color='success')
    ])
