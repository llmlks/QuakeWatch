import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as clrs
import matplotlib.pyplot as plt

color_map = cm.get_cmap('brg')


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
    """Return an array of colors, one for each row of data, and
    a dictionary for building a colorbar.
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
        colors = np.repeat('red', data.shape[0])
        color_domain = None
    else:
        colors = data[color_column]
        color_domain = dict(
            domainMin=colors.min(),
            domainMax=colors.max(),
            colorscale=[
                clrs.to_hex(color_map(c)) for c in [0, 0.25, 0.5, 0.75, 0.99]
            ]
        )

        if colors.min() <= 0:
            colors -= colors.min()

        if colors.max() > 1:
            colors /= colors.max()

        colors = [clrs.to_hex(color_map(c)) for c in colors]

    return colors, color_domain
