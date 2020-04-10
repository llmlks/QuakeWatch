import dash_core_components as dcc
import dash_html_components as html
import numpy as np

HALF_MAX_SIZE = 1000


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


def get_sizes(data, normalized_sizes=None):
    """Return an array of sizes, one for each row of data.

    Select correct values from normalized sizes using the
    index values from the data frame. Add 0.1 to the values
    before multiplying to get the final sizes to ensure non-
    zero sizes, as the values are given in the range [0, 1].
    If the normalized sizes array is None, return an array
    filled with default values.

    Keyword arguments:
    data -- Dataframe object containing the filtered data
    normalized_sizes -- A numpy array containing normalized
        values to use for sizes
    """
    if normalized_sizes is None:
        return np.repeat(200, data.shape[0])

    sizes = np.take(normalized_sizes, data.index.to_numpy())
    sizes += 0.1

    return sizes * HALF_MAX_SIZE
