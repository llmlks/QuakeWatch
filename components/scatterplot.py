import dash_html_components as html
import dash_core_components as dcc

from utils import earthquake_data


def get_graph(session_id, min_time, max_time, x_axis, y_axis, color, size):
    """Return a scatterplot with example points.

    Keywords arguments:
    session_id -- ID of the current session
    min_time -- A datetime object representing the start of the time frame
    max_time -- A datetime object representing the end of the time frame
    x_axis -- A pandas Series of the x-axis values
    y_axis -- A pandas Series of the y-axis values
    color -- A pandas Series of the marker color values
    size -- A pandas Series of the marker sizes
    """

    return dcc.Graph(
        # The size is 10 times to make points visible for this example
        figure={
            'data': [
                {'x': x_axis, 'y': y_axis, 'mode': 'markers',
                    'marker': {'size': size*10, 'color': color}}
            ],
            'layout': {
                'title': 'Scatterplot',
                'xaxis': {
                    'title': 'Date'
                },
                'yaxis': {
                    'title': 'Depth'
                }
            }
        }
    )


def get_component(session_id, min_time, max_time, x_axis, y_axis, color, size):
    """
    Return the scatterplot component.

    Keywords arguments:
    session_id -- ID of the current session
    min_time -- A datetime object representing the start of the time frame
    max_time -- A datetime object representing the end of the time frame
    x_axis -- A pandas Series of the x-axis values
    y_axis -- A pandas Series of the y-axis values
    color -- A pandas Series of the marker color values
    size -- A pandas Series of the marker sizes
    """
    return html.Div([
        get_graph(session_id, min_time, max_time, x_axis, y_axis, color, size)
    ])


def update_output(session_id, min_time, max_time, x_axis, y_axis, color, size):
    return get_graph(
        session_id, min_time, max_time, x_axis, y_axis, color, size
    )
