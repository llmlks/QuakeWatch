from datetime import datetime, timedelta

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from components import quake_map
from components import time_slider
from components.config import map_config
from components.config.timestep_picker import DEFAULT_TIMESTEP
from utils import earthquake_data


def get_layout(session_id):
    """Return map layout with interactive map, time slider and configuration.

    This method draws the earthquakes that happened during the first week of
    the data. To update the map, use method `update_map`.

    Keyword arguments:
    session_id -- ID of the current session
    """

    eq_data = earthquake_data.get_earthquake_data(session_id)
    start_date, end_date = eq_data.get_daterange()
    default_end_date = start_date + timedelta(weeks=1)

    filtered_data = filter_data(eq_data, start_date, DEFAULT_TIMESTEP, 0)

    return html.Div([
        dbc.Row(
            [
                dbc.Col(html.Div(
                    id='map-wrapper',
                    children=[quake_map.get_component(filtered_data)]
                )),
                dbc.Col(map_config.get_component(
                    start_date, end_date, default_end_date)
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    id='slider-wrapper',
                    children=[time_slider.get_component(
                        start_date, default_end_date, DEFAULT_TIMESTEP
                    )]))
            ]
        )

    ])


def filter_data(eq_data, start_date, timestep, slider_value):
    """Filter data based on the given arguments.

    Keyword arguments:
    eq_data -- EarthquakeData object that contains the unfiltered data.
    start_date --  Datetime object representing the start of the time frame
    timestep -- The timestep as seconds. Earthquakes that happened within
        a time window of this size are returned.
    slider_value -- The value of the time slider. Controls the temporal
        position of the time window for which earthquakes are shown.
    """
    start_time = start_date + timedelta(seconds=slider_value*timestep)
    end_time = start_time + timedelta(seconds=timestep)

    return eq_data.filter_by_dates(start_time, end_time)


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
    """Update the map based on the slider position and the configuration.

    This is a callback function invoked by changes to either the time slider
    or the configuration.

    Keyword arguments:
    slider_value -- The value of the current slider position.
        Between 0 and steps-1.
    apply_clicks -- The number of clicks on the apply button.
    session_id -- ID of the current session
    start_date -- String from the date picker representing the start date
    end_date -- String from the date picker representing the end date
    timestep_value -- The time step in some time unit. Earthquakes that
        happened within the time window of this size are shown.
    timestep_seconds -- The number of seconds the selected time unit is
        equal to
    """

    timestep = timestep_seconds * timestep_value
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)

    eq_data = earthquake_data.get_earthquake_data(session_id)
    filtered_data = filter_data(eq_data, start_date, timestep, slider_value)

    return quake_map.get_component(filtered_data)


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
    """Update the time slider based on the configuration.

    This is a callback function invoked by changes to the configuration.

    Keyword arguments:
    apply_clicks -- The number of clicks on the apply button.
    session_id -- ID of the current session
    start_date -- String from the date picker representing the start date
    end_date -- String from the date picker representing the end date
    timestep_value -- The time step in some time unit. Earthquakes that
        happened within the time window of this size are shown.
    timestep_seconds -- The number of seconds the selected time unit is
        equal to
    """
    if apply_clicks is None:
        raise PreventUpdate

    timestep = timestep_seconds * timestep_value
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)

    return time_slider.get_component(
        start_date, end_date, timestep
    )
