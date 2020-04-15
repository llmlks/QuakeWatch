import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import axis_picker
from components.config import date_picker


def get_component(columns, min_date, max_date, default_end_date):

    return html.Div([
        date_picker.get_component(min_date, max_date, default_end_date),
        axis_picker.get_component(columns, None),
        dbc.Button('Apply', id='apply', outline=True, color='success')
    ])
