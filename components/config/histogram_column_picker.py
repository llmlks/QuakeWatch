import dash_core_components as dcc
import dash_html_components as html


def get_component(columns):
    return html.Div(children=[
        html.Div(children='Column'),
        dcc.Dropdown(
            id='column',
            clearable=False,
            searchable=True,
            options=[
                {'label': column, 'value': column}
                for column in columns
            ],
        )
    ])
