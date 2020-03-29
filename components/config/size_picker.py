import dash_core_components as dcc
import dash_html_components as html
import numpy as np


def get_component(columns):
    """Return size picker component.

    Keyword arguments:
    columns -- The columns available in the uploaded data
    """

    return html.Div(children=[
        html.Div(className='config-label', children='Size column'),
        dcc.Dropdown(
            id='size-column',
            clearable=True,
            searchable=True,
            options=[
                {'label': column, 'value': column}
                for column in columns
            ],
            value=None
        )
    ])


def get_sizes(data, size_column):
    """Return an array of sizes, one for each row of data.
    If the size column argument is None, default size is
    used instead.

    Keyword arguments:
    data -- Dataframe object
    size_column -- Column to use for calculating the sizes,
        or None for default values
    """
    if size_column is None:
        sizes = np.repeat(200, data.shape[0])
    else:
        sizes = data[size_column]
        if sizes.min() <= 0:
            sizes += 1 - sizes.min()

        while sizes.min() < 100:
            sizes *= 10

        while sizes.min() > 2000:
            sizes /= 5

    return sizes
