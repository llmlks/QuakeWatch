import dash_html_components as html
import dash_core_components as dcc

from utils import earthquake_data
from components.config import axis_picker
from components.config import date_picker


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
