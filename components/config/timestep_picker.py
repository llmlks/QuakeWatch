import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

DEFAULT_TIMESTEP = 24*60*60


def get_component():
    """Return the timestep picker component."""

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
              {'label': 'Hours', 'value': 60*60},
              {'label': 'Days', 'value': 24*60*60},
              {'label': 'Weeks', 'value': 7*24*60*60},
            ],
            value=DEFAULT_TIMESTEP
        )
    ], title='Select the unit and value of time for one frame in the map.'
       ' One frame will show all the earthquakes that occurred within '
       'the selected time.'
    )
