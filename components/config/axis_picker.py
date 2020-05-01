import dash_core_components as dcc
import dash_html_components as html


def get_component(columns, default_value, x_axis=True, is_histogram=False):
    """Return an axis picker component.

    Keyword arguments:
    columns -- The columns available in the uploaded data
    default_value -- Name of the column selected by default
    x_axis -- Boolean, whether the axis to pick is the x axis
    """
    label = is_histogram and 'column' or ((x_axis and 'x-axis') or 'y-axis')

    return html.Div(children=[
        html.Div(className='config-label', children=label.capitalize()),
        dcc.Dropdown(
            id=label,
            clearable=False,
            searchable=True,
            options=[
                {'label': column, 'value': column}
                for column in columns
            ],
            value=default_value
        )
    ])
