import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

from utils import earthquake_data


def get_component(xaxis, yaxis, session_id):
    """ Return a heatmap with the given configuration.

    Keyword components:
    xaxis -- a pandas Series of the xaxis values
    yaxis -- a pandas Series of the yaxis values
    """

    nbins = 6

    eq_data = earthquake_data.get_earthquake_data(session_id)
    data = eq_data.data.filter(items=[xaxis.name, yaxis.name])

    xcats, xbins = pd.cut(data[xaxis.name], nbins, retbins=True)
    ycats, ybins = pd.cut(data[yaxis.name], nbins, retbins=True)

    z = data.groupby([xcats, ycats]).size().unstack()

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
