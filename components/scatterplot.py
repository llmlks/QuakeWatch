import dash_html_components as html
import dash_core_components as dcc

from utils import earthquake_data


def get_component(x_axis, y_axis, event_ids, color, size, size_data):
    """Return a scatterplot with given configurations.

    Keyword arguments:
    x_axis -- A pandas Series of the x-axis values
    y_axis -- A pandas Series of the y-axis values
    event_ids -- A pandas Series of the event ids of the nodes
    color -- A pandas Series of the marker color values, or a string for one
        color
    size -- An iterable of the marker sizes
    size_data -- A pandas Series containing the data used to determine the
        marker sizes
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
                },
                'text': get_hover_text(color, event_ids, size_data)
            }],
            'layout': {
                'title': 'Scatter plot',
                'xaxis': {
                    'title': x_axis.name
                },
                'yaxis': {
                    'title': y_axis.name
                },
                'hovermode': 'closest'
            }
        }
    )


def get_hover_text(color, event_ids, size_data):
    """Return a pandas Series that contains the text shown when you hover over
    a node. The hover text contains the values of the selected columns.

    Keyword arguments:
    color -- A pandas Series of the marker color values, or a string for one
        color
    event_ids -- A pandas Series of the event ids of the nodes
    size_data -- A pandas Series containing the data used to determine the
        marker sizes
    """
    hover_text = ""
    if (size_data is not None):
        hover_text += size_data.name + ': ' + size_data.astype(str) + '<br>'
    if (type(color) != str):
        hover_text += color.name + ': ' + color.astype(str) + '<br>'
    hover_text += event_ids.name + ': ' + event_ids.astype(str)
    return hover_text
