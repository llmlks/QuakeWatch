import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl

from app import app


api_base_url = 'https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?'
api_url = api_base_url + 'apikey=' + app.server.config['THUNDERFOREST_API_KEY']

attribution = """Maps &copy;
<a href="http://www.thunderforest.com">Thunderforest</a>
, Data &copy;
<a href="http://www.openstreetmap.org/copyright">
OpenStreetMap contributors</a>"""


def get_component():
    """
    Return the map component.
    """
    return html.Div([
        dl.Map(
            center=[33.7, -117.3],
            zoom=8,
            children=[
                dl.TileLayer(
                    url=api_url,
                    attribution=attribution)
            ])
    ])
