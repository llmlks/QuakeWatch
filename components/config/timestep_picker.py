import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


def get_component():
    return html.Div(children=[
        html.Div(className='config-label', children='Timestep'),
        dbc.Input(id='timestep-value', type='number', min=1, step=1, value=1),
        dcc.Dropdown(
            id='timestep-unit',
            clearable=False,
            searchable=False,
            options=[
              {'label': 'Seconds', 'value': 1},
              {'label': 'Minutes', 'value': 60},
            ],
            value=1
        )
    ])
