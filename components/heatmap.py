import dash_html_components as html
import dash_core_components as dcc
import numpy as np

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
                {'z': z.values, 'x': xbins, 'y': ybins, 'type': 'heatmap',
                 'text': get_hover_text(z, xbins, ybins),
                 'hoverinfo': 'text'},
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


def get_hover_text(z, xbins, ybins):
    """ Return an array of strings to work as hoverinfo for the heatmap

    Keyword arguments:
    z -- Weight vector of the heatmap
    xbins -- The bins used for the x-axis
    ybins -- The bins used for the y-axis
    """
    z_hover = np.empty((len(xbins)-1, len(ybins)-1), dtype=object)
    for i in range(len(xbins)-1):
        for j in range(len(ybins)-1):
            z_hover[i, j] = (xbins.name + ": [" + xbins[i].astype(str) +
                             ", " + xbins[i+1].astype(str) + "] <br>" +
                             ybins.name + ": [" + ybins[j].astype(str) +
                             ", " + ybins[j+1].astype(str) + "] <br>" +
                             "Count: " + z.values[i][j].astype(str))
    return z_hover
