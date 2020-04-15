import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from components import histogram
from utils import earthquake_data
from components.config import axis_picker
from components.config import date_picker
from components.config import histogram_config
from dash.exceptions import PreventUpdate
from app import app


def get_layout(session_id):
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is None or eq_data.data.shape == (0, 0):
        return 'No uploaded data found'

    return html.Div([
            dbc.Col(
                html.Div(
                    id='histogram',
                    children=histogram.get_component(None)
                )
            ),
            dbc.Col(histogram_config.get_component(eq_data.data.columns))
    ])


@app.callback(
    Output('histogram', 'children'),
    [Input('apply', 'n_clicks')],
    [State('session-id', 'children'),
     State('x-axis', 'value')])
def update_output(clicks, session_id, x_axis):
    if clicks is None:
        raise PreventUpdate

    eq_data = earthquake_data.get_earthquake_data(session_id)
    x_axis = eq_data.data[x_axis]
    return histogram.get_component(x_axis)
