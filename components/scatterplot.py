import dash_html_components as html
import dash_core_components as dcc

from utils import earthquake_data


def get_component(x_axis, y_axis, color, size):
    """Return a scatterplot with given configurations.

    Keyword arguments:
    x_axis -- A pandas Series of the x-axis values
    y_axis -- A pandas Series of the y-axis values
    color -- An iterable of the marker color values, or a string for one color
    size -- An iterable of the marker sizes
    """
    if type(color) == str:
        show_scale = False
    else:
        show_scale = True

    return dcc.Graph(
        figure={
            'data': [{
                'x': x_axis, 'y': y_axis, 'mode': 'markers',
                'marker': {
                    'size': size, 'color': color, 'showscale': show_scale
                }
            }],
            'layout': {
                'title': 'Scatterplot',
                'xaxis': {
                    'title': x_axis.name
                },
                'yaxis': {
                    'title': y_axis.name
                }
            }
        }
    )
