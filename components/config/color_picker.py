import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as clrs
import matplotlib.pyplot as plt
import plotly.express as px

color_map = cm.get_cmap('brg')
cmap = px.colors.cyclical.hsv


def get_component(columns):
    """Return color picker component.

    Keyword arguments:
    columns -- The columns available in the uploaded data
    """

    return html.Div(children=[
        html.Div(className='config-label', children='Color column'),
        dcc.Dropdown(
            id='color-column',
            clearable=True,
            searchable=True,
            options=[
                {'label': column, 'value': column}
                for column in columns
            ],
            value=None
        )
    ])


def get_colors(data, color_column):
    """Return an array of colors, one for each row of data.
    If the color column argument is None, default color 'red' is
    used instead.

    The values in the given column are normalized to the range
    [0,1], and the result is used to extract a color from a
    colormap.

    Keyword arguments:
    data -- Dataframe object
    color_column -- Column to use for calculating the colors,
        or None for default values
    """
    if color_column is None:
        colors = np.repeat('red', eq_data.data.shape[0])
    else:
        colors = eq_data.data[color_column]
        if colors.min() <= 0:
            colors -= colors.min()

        if colors.max() > 1:
            colors /= colors.max()

        colors = [clrs.to_hex(color_map(c)) for c in colors]

    return colors
