import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import date_picker
from components.config import timestep_picker


def get_component(min_date, max_date):
    return html.Div([
        date_picker.get_component(min_date, max_date),
        timestep_picker.get_component(),
        dbc.Button("Apply", id='apply', outline=True,
                    color="success")
    ])
