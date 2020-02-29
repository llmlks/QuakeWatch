import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl


api_url = 'https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=4853a161887243a8acbda32784c26748'
attribution = """Maps &copy;
<a href="http://www.thunderforest.com">Thunderforest</a>
, Data &copy;
<a href="http://www.openstreetmap.org/copyright">
OpenStreetMap contributors</a>"""


def get_component():
    """"""
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
