import dash_html_components as html
import dash_core_components as dcc


def get_component(column, nbins):
    """ Return a histogram with the given configuration.

    Keyword components:
    column -- a pandas Series of the column values
    nbins -- Maximum number of bins used
    """
    return dcc.Graph(
        figure={
            'data': [
                {'x': column, 'type': 'histogram',
                 'nbinsx': nbins - 1, 'name': 'column'},
            ],
            'layout': {
                'title': 'Histogram'
            }
        }
    )
