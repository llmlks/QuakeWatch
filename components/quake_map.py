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


def get_component(eq_data, sizes, opacities, color_params=None,
                  show_uncertainties=False, show_faults=False):
    """Return the map component with earthquakes represented as circles.

    Keyword arguments:
    eq_data -- EarthquakeData object containing the quakes to be drawn.
    sizes -- An array containing a size for each data point
    opacities -- An array containing an opacity for each data point
    color_params -- A tuple with the column name and its minimum
        and maximum values for extracting and normalizing values
        to use for colors
    show_uncertainties -- A boolean indicating whether to display the
        uncertainties in location of each data point
    show_faults -- A boolean indicating whether to show the faults
    """

    colors, color_domain = get_colors(eq_data.data, color_params)

    return dl.Map(
        id='quake-map',
        center=eq_data.get_map_center(),
        zoom=eq_data.get_initial_zoom(),
        children=[
            dl.TileLayer(
                url=api_url,
                attribution=attribution),
            html.Div(id='test-id', children=[
                get_fault_layer(show_faults),
                get_event_layer(eq_data, sizes, colors, opacities),
                get_location_uncertainty_layer(
                    eq_data, show_uncertainties
                )
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


def get_event_layer(eq_data, sizes, colors, opacities):
    """Return a LayerGroup that contains earthquakes represented as circles.

    Keyword arguments:
    eq_data -- EarthquakeData object containing the quakes to be drawn.
    sizes -- An array containing a size for each data point
    colors -- An array containing a color for each data point
    opacities -- An array containing an opacity for each data point
    """

    quake_circles = [
        dl.Circle(
            center=[quake['LATITUDE'], quake['LONGITUDE']],
            radius=sizes[idx],
            color=colors[idx],
            fillOpacity=opacities[idx],
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


def get_location_uncertainty_layer(eq_data, visible):
    """Return a map layer with uncertainties visualized for each data point.

    Keyword arguments:
    eq_data -- An Earthquake data object containing the data visible on the map
    visible -- A boolean indicating whether to display the uncertainties in
        location of each data point
    """
    if eq_data.data.shape[0] == 0 or not visible:
        return dl.LayerGroup(id='location-uncertainties')

    location_uncertainties = eq_data.get_location_uncertainties()
    reset_data = eq_data.data.reset_index()
    uncertainties = []

    if type(location_uncertainties) == int:
        uncertainties = [
            dl.Circle(
                center=[quake['LATITUDE'], quake['LONGITUDE']],
                radius=location_uncertainties,
                color='black',
                fillOpacity=0,
                dashArray='5, 5',
                weight=1.5,
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
            for _, quake in reset_data.iterrows()
        ]

    else:
        uncertainties += [
            dl.Polyline(
                positions=[
                    [quake['LATITUDE'], quake['LONGITUDE']],
                    location_uncertainties[idx + direction*reset_data.shape[0]]
                ],
                color='black',
                dashArray='5, 5',
                weight=1.5
            )
            for direction in range(4)
            for idx, quake in reset_data.iterrows()
        ]

    return dl.LayerGroup(id='location-uncertainties', children=uncertainties)


def get_fault_layer(show_faults=False):
    """Return a LayerGroup that contains the Southern California
    fault lines as PolyLines.

    Blind faults are represented by dashed, dark grey lines and
    non-blind faults by solid, black lines.

    Keyword arguments:
    show_faults -- A boolean indicating whether to show the faults
    """
    if show_faults:
        return fault_layer
    return dl.LayerGroup(id='fault-layer', children=[])


def create_fault_layer():
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


fault_layer = create_fault_layer()
