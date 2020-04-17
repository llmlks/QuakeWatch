import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

DEFAULT_TIMESTEP = 24*60*60


def get_component():
    """Return the timestep picker component."""

    return html.Div(children=[
        dbc.Checklist(
            id='uncertainty-toggle',
            options=[{
                'label': 'Visualize location uncertainties',
                'value': 1
            }],
            value=[],
            switch=True,
        )
    ])
