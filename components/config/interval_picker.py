import dash_html_components as html
import dash_bootstrap_components as dbc


def get_component():
    """Return the interval picker component"""
    return html.Div(
        children=[
            html.Div(
                className='config-label',
                children='Update interval for "Play" button'
            ),
            dbc.Input(
                id='interval-seconds', type='number', min=1, step=0.5, value=2
            ),
            html.Div('Seconds', style={'display': 'inline-block'})
        ],
        title='The update frequency of the "Play" -feature in seconds.'
        '\nNB: A small value may cause lagging'
    )
