import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


def get_component():
    """Return the uncertainty toggler component."""

    return html.Div(children=[
        dbc.Checklist(
            id='uncertainty-toggle',
            className='toggle-select',
            options=[{
                'label': 'Visualize location uncertainties',
                'value': 1
            }],
            value=[],
            switch=True,
        )
    ])
