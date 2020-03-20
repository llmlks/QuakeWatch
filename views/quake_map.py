from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from components import quake_map
from components import time_slider
from components.config import map_config

# TODO: Get these from the user configuration
min_time = datetime(2008, 1, 1, 0, 4)
max_time = datetime(2008, 1, 9, 5)
time_step = 86400


def get_layout(session_id):
    return html.Div([
        dbc.Row(
            [
                dbc.Col(html.Div(
                    id='map-wrapper',
                    children=[quake_map.get_component(
                        min_time, max_time, time_step, 0, session_id
                    )])),
                dbc.Col(map_config.get_component(min_time, max_time))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    id='slider-wrapper',
                    children=[time_slider.get_component(
                        min_time, max_time, time_step
                    )]))
            ]
        )

    ])


@app.callback(
    Output('map-wrapper', 'children'),
    [Input('time-slider', 'value'),
     Input('apply', 'n_clicks'),
     Input('session-id', 'children')],
    [State('date-pick', 'start_date'),
     State('date-pick', 'end_date'),
     State('timestep-value', 'value'),
     State('timestep-unit', 'value')])
def update_map(slider_value, apply_clicks, session_id, start_date, end_date,
               timestep_value, timestep_seconds):
    if apply_clicks is None:
        raise PreventUpdate
    timestep = timestep_seconds * timestep_value
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    return quake_map.get_component(
        start_date, end_date, timestep, slider_value, session_id
    )


@app.callback(
    Output('slider-wrapper', 'children'),
    [Input('apply', 'n_clicks'),
     Input('session-id', 'children')],
    [State('date-pick', 'start_date'),
     State('date-pick', 'end_date'),
     State('timestep-value', 'value'),
     State('timestep-unit', 'value')])
def update_time_slider(apply_clicks, session_id, start_date, end_date,
                       timestep_value, timestep_seconds):
    if apply_clicks is None:
        raise PreventUpdate
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    timestep = timestep_seconds * timestep_value
    return time_slider.get_component(
        start_date, end_date, timestep
    )
