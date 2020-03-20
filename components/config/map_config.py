import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import date_picker


def get_component(min_date, max_date):
    return html.Div([
        date_picker.get_component(min_date, max_date),
        dbc.Button("Apply", id='apply', outline=True,
                    color="success", size="sm"),
        html.Div(id='temp')
    ])
