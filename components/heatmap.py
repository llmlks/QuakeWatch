import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

from utils import earthquake_data


def get_component(z, xbins, ybins):
    """ Return a heatmap with the given configuration.

    Keyword components:
    xaxis -- a pandas Series of the xaxis values
    yaxis -- a pandas Series of the yaxis values
    """

    return dcc.Graph(
        figure={
            'data': [
                {'z': z.values, 'x': xbins, 'y': ybins, 'type': 'heatmap'},
            ],
            'layout': {
                'title': 'Heatmap'
            }
        }
    )
