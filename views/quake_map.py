from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from components import quake_map
from components import time_slider

# TODO: Get these from the user configuration
min_time = datetime(2008, 1, 1, 0, 4)
max_time = datetime(2008, 1, 9, 5)
time_step = 86400


def get_layout(session_id):
    return html.Div([
        html.Div(
            id='map-wrapper',
            children=[quake_map.get_component(
                min_time, max_time, time_step, 0, session_id
            )]),
        time_slider.get_component(min_time, max_time, time_step)
    ])


@app.callback(
    Output('map-wrapper', 'children'),
    [Input('time-slider', 'value'),
     Input('session-id', 'children')])
def update_map(value, session_id):
    return quake_map.get_component(
        min_time, max_time, time_step, value, session_id
    )
