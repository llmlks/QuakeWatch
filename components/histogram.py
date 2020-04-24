import dash_html_components as html
import dash_core_components as dcc


def get_component(column):
    """ Return a histogram with the given configuration.

    Keyword components:
    column -- a pandas Series of the column values
    """
    return dcc.Graph(
        figure={
            'data': [
                {'x': column, 'type': 'histogram',
                 'name': 'column'},
            ],
            'layout': {
                'title': 'Histogram'
            }
        }
    )
