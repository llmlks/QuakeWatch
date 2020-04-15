import dash_core_components as dcc
import dash_html_components as html
import numpy as np

MAP_MAX_SIZE = 1000
PLOT_MAX_SIZE = 50


def get_component(columns, default_value=None):
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
            value=default_value
        )
    ])


def get_sizes(data, column_params=None, is_map=True):
    """Return an array of sizes, one for each row of data.

    The values in the given column are normalized to the range
    ]0,1] using the given minimum and maximum values. 0.1 is
    added to the values before dividing by the maximum to
    ensure non-zero sizes.

    If the column parameters argument is None, return an array
    filled with default values.

    Keyword arguments:
    data -- Dataframe object containing the filtered data
    column_params -- A tuple with the column name and its minimum
        and maximum values for extracting and normalizing values
        to use for sizes
    """
    if column_params is None:
        default_size = 200
        if not is_map:
            default_size = 10
        return np.repeat(default_size, data.shape[0])

    name, minimum, maximum = column_params

    sizes = data[name].astype(float).copy()

    sizes += 0.1 - minimum
    sizes /= (maximum - minimum + 0.1)
    sizes = np.array([0.5 if np.isnan(size) else size for size in sizes])

    scalar = MAP_MAX_SIZE
    if not is_map:
        scalar = PLOT_MAX_SIZE

    return sizes * scalar
