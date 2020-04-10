import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl
import shapefile

from app import app
from utils import earthquake_data


api_url = 'https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?' \
    + 'apikey=' + app.server.config['THUNDERFOREST_API_KEY']

attribution = """Maps &copy;
<a href="http://www.thunderforest.com">Thunderforest</a>
, Data &copy;
<a href="http://www.openstreetmap.org/copyright">
OpenStreetMap contributors</a>"""

faults_blind = './shapefiles/CFM52_preferred_traces_blind.shp'
faults_nonblind = './shapefiles/CFM52_preferred_traces_nonblind.shp'


def get_component(eq_data):
    """Return the map component with earthquakes represented as circles.

    Keyword arguments:
    eq_data -- EarthquakeData object containing the quakes to be drawn.
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
                get_fault_layer(),
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


def get_fault_layer():
    """Return a LayerGroup that contains the Southern California
    fault lines as PolyLines.

    Blind faults are represented by dashed, dark grey lines and
    non-blind faults by solid, black lines.
    """
    blind_faults = shapefile.Reader(faults_blind)
    nonblind_faults = shapefile.Reader(faults_nonblind)

    faults = [
        dl.Polyline(
            color='#404040',
            weight=1.25,
            dashArray='2, 3',
            positions=[
                [coord[1], coord[0]]
                for coord in feature.shape.__geo_interface__['coordinates']
            ]
        )
        for feature in blind_faults.shapeRecords()
    ]

    faults += [
        dl.Polyline(
            color='black',
            weight=1,
            positions=[
                [coord[1], coord[0]]
                for coord in feature.shape.__geo_interface__['coordinates']
            ]
        )
        for feature in nonblind_faults.shapeRecords()
    ]

    return dl.LayerGroup(id='fault-layer', children=faults)
