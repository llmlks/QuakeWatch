import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import timedelta

from components import histogram
from components.config import histogram_config
from utils import earthquake_data
from app import app


def get_layout(session_id):
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is None or eq_data.data.shape == (0, 0):
        return 'No uploaded data found'

    start_date, end_date = eq_data.get_daterange()
    default_end_date = start_date + timedelta(weeks=1)
    filtered_data = eq_data.filter_by_dates(start_date, default_end_date)

    default_size_column = eq_data.get_column_params(
        eq_data.get_magnitudes().name
    )

    return html.Div([
            dbc.Col(
                html.Div(
                    id='histogram',
                    children=histogram.get_component(None)
                )
            ),
            dbc.Col(histogram_config.get_component(
                eq_data.data.columns, start_date, end_date, default_end_date))
    ])


@app.callback(
    Output('histogram', 'children'),
    [Input('apply', 'n_clicks')],
    [State('session-id', 'children'),
     State('column', 'value'),
     State('date-pick', 'start_date'),
     State('date-pick', 'end_date')])
def update_output(clicks, session_id, x_axis, start_date, end_date):
    if clicks is None:
        raise PreventUpdate

    eq_data = earthquake_data.get_earthquake_data(session_id)
    filtered_data = eq_data.filter_by_dates(start_date, end_date)

    x_axis = filtered_data.data[x_axis]
    return histogram.get_component(x_axis)
