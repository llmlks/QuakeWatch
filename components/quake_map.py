import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl
import shapefile
import dash_table

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

faults_blind = './shapefiles/CFM52_preferred_traces_blind.shp'
faults_nonblind = './shapefiles/CFM52_preferred_traces_nonblind.shp'


def get_component(eq_data, sizes, color_column=None):
    """Return the map component with earthquakes represented as circles.

    Keyword arguments:
    eq_data -- EarthquakeData object containing the quakes to be drawn.
    sizes -- An array containing a size for each data point
    color_column -- The column for computing the color of each data point
    """

    colors, color_domain = get_colors(eq_data.data, color_column)

    return dl.Map(
        id='quake-map',
        center=eq_data.get_map_center(),
        zoom=eq_data.get_initial_zoom(),
        children=[
            dl.TileLayer(
                url=api_url,
                attribution=attribution),
            html.Div(id='test-id', children=[
                get_fault_layer(),
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
            weight=2,
            children=[dl.Popup(
                dcc.Markdown(
                    list(map(
                        lambda x: '**{}**: {}  '.format(
                            x.replace('[', r'\['), quake[x]
                        ),
                        quake.keys()
                    ))
                ),
                className='earthquake-popup'
            )]
        )
        for idx, quake in eq_data.data.reset_index().iterrows()]

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
