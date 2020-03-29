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


def get_component(eq_data):
    """Return the map component with earthquakes represented as circles.

    Keyword arguments:
    eq_data -- EarthquakeData object containing the quakes to be drawn.
    """

    return dl.Map(
        id='quake-map',
        center=eq_data.get_map_center(),
        zoom=eq_data.get_initial_zoom(),
        children=[
            dl.TileLayer(
                url=api_url,
                attribution=attribution),
            html.Div(id='test-id', children=[
                get_event_layer(
                        eq_data
                )])
        ])


def get_event_layer(eq_data):
    """Return a LayerGroup that contains earthquakes represented as circles.

    Keyword arguments:
    eq_data -- EarthquakeData object containing the quakes to be drawn.
    """

    quake_circles = [
        dl.Circle(
            center=[quake['LATITUDE'], quake['LONGITUDE']],
            radius=100,
            color='red',
            fillOpacity=0.1,
            weight=2
        )
        for _, quake in eq_data.data.iterrows()]

    return dl.LayerGroup(id='layer-id', children=quake_circles)
