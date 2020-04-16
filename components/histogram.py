import dash_html_components as html
import dash_core_components as dcc


def get_component(x_axis):
    return dcc.Graph(
        figure={
            'data': [
                {'x': x_axis, 'type': 'histogram',
                 'name': 'column'},
            ],
            'layout': {
                'title': 'Histogram'
            }
        }
    )
