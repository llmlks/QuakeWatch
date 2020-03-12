from datetime import timedelta

import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl

from app import app
from utils import earthquake_data


api_url = 'https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?' \
    + 'apikey=' + app.server.config['THUNDERFOREST_API_KEY']

attribution = """Maps &copy;
<a href="http://www.thunderforest.com">Thunderforest</a>
, Data &copy;
<a href="http://www.openstreetmap.org/copyright">
OpenStreetMap contributors</a>"""


def get_component(min_time, max_time, time_step, slider_value, session_id):
    """Return the map component with earthquakes represented as circles.

    Keyword arguments:
    min_time -- A datetime object representing the start of the time frame
    max_time -- A datetime object representing the end of the time frame
    time_step -- The time step as seconds. Earthquakes that happened within
        the time window of this size are shown.
    slider_value -- The value of the time slider. Controls the temporal
        position of the time window for which earthquakes are shown.
    session_id -- ID of the current session
    """

    return dl.Map(
        id='quake-map',
        center=[33.7, -117.3],
        zoom=8,
        children=[
            dl.TileLayer(
                url=api_url,
                attribution=attribution),
            html.Div(id='test-id', children=[
                get_event_layer(
                        min_time, max_time, time_step, slider_value, session_id
                )])
        ])


def get_event_layer(min_time, max_time, time_step, slider_value, session_id):
    """Return a LayerGroup that contains earthquakes represented as circles.

    The shown earthquake events are selected based on the argument values.

    Keyword arguments:
    min_time -- A datetime object representing the start of the time frame
    max_time -- A datetime object representing the end of the time frame
    time_step -- The time step as seconds. Earthquakes that happened within
        the time window of this size are shown.
    slider_value -- The value of the time slider. Controls the temporal
        position of the time window for which earthquakes are shown.
    session_id -- ID of the current session
    """
    start_time = min_time + timedelta(seconds=slider_value*time_step)
    end_time = start_time + timedelta(seconds=time_step)

    data = earthquake_data.get_earthquake_data(session_id).data
    datetimes = earthquake_data.get_datetimes(data)
    filtered_quakes = data[(datetimes > start_time) & (datetimes < end_time)]

    quake_circles = [
        dl.Circle(
            center=[quake['LATITUDE'], quake['LONGITUDE']],
            radius=100,
            color='red',
            fillOpacity=0.1,
            weight=2
        )
        for _, quake in filtered_quakes.iterrows()]

    return dl.LayerGroup(id='layer-id', children=quake_circles)
