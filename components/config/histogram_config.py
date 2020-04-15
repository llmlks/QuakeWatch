import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import axis_picker


def get_component(columns):

    return html.Div([
        axis_picker.get_component(columns, None),
        dbc.Button('Apply', id='apply', outline=True, color='success')
    ])
