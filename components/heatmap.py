import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

from utils import earthquake_data


def get_component(z, xbins, ybins):
    """ Return a heatmap with the given configuration.

    Keyword components:
    z -- Weight vector of the heatmap
    xbins -- The bins used for the x-axis
    ybins -- The bins used for the y-axis
    """

    return dcc.Graph(
        figure={
            'data': [
                {'z': z.values, 'x': xbins, 'y': ybins, 'type': 'heatmap'},
            ],
            'layout': {
                'title': 'Heatmap',
                'xaxis': {
                    'title': xbins.name
                },
                'yaxis': {
                    'title': ybins.name
                },
                'hovermode': 'closest'
            }
        }
    )
