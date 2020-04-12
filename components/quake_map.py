import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl

from app import app
from utils import earthquake_data
from components.config.color_picker import get_colors


api_url = 'https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?' \
    + 'apikey=' + app.server.config['THUNDERFOREST_API_KEY']

attribution = """Maps &copy;
<a href="http://www.thunderforest.com">Thunderforest</a>
, Data &copy;
<a href="http://www.openstreetmap.org/copyright">
OpenStreetMap contributors</a>"""


def get_component(eq_data, sizes, color_params=None):
    """Return the map component with earthquakes represented as circles.

    Keyword arguments:
    eq_data -- EarthquakeData object containing the quakes to be drawn.
    sizes -- An array containing a size for each data point
    color_params -- A tuple with the information for extracting and
        normalizing values to use for colors
    """

    colors, color_domain = get_colors(eq_data.data, color_params)

    return dl.Map(
        id='quake-map',
        center=[33.7, -117.3],
        zoom=8,
        children=[
            dl.TileLayer(
                url=api_url,
                attribution=attribution),
            html.Div(id='test-id', children=[
                get_event_layer(eq_data, sizes, colors)
            ]),
            (color_domain is not None and dl.Colorbar(
                width=200,
                height=20,
                **color_domain,
                style={
                    'color': 'black',
                    'font-weight': 'bold'
                }
            ))
        ])


def get_event_layer(eq_data, sizes, colors):
    """Return a LayerGroup that contains earthquakes represented as circles.

    Keyword arguments:
    eq_data -- EarthquakeData object containing the quakes to be drawn.
    sizes -- An array containing a size for each data point
    colors -- An array containing a color for each data point
    """

    quake_circles = [
        dl.Circle(
            center=[quake['LATITUDE'], quake['LONGITUDE']],
            radius=sizes[idx],
            color=colors[idx],
            fillOpacity=0.3,
            weight=2
        )
        for idx, quake in eq_data.data.reset_index().iterrows()]

    return dl.LayerGroup(id='layer-id', children=quake_circles)
