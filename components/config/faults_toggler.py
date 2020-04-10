import dash_bootstrap_components as dbc
import dash_html_components as html


def get_component(visible):
    """Return the Southern California faults toggler component.

    Keyword arguments:
    visible -- A boolean indicating whether the configuration should
        be visible
    """

    display_style = {}
    if not visible:
        display_style = {'display': 'none'}

    return html.Div(children=[
        dbc.Checklist(
            id='faults-toggle',
            className='toggle-select',
            options=[{
                'label': 'Show fault lines',
                'value': 1
            }],
            value=[],
            switch=True,
        )
    ], style=display_style)
