from datetime import datetime
from dash.dependencies import Input, Output

from components import scatterplot
from utils import earthquake_data
from app import app


def get_layout(session_id):
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is None or eq_data.data.shape == (0, 0):
        return 'No data found'

    # TODO: Get these from user configuration
    min_time = datetime(2008, 1, 1, 0, 4)
    max_time = datetime(2008, 1, 9, 5)
    x_axis = eq_data.get_datetimes()
    y_axis = eq_data.get_depths()
    color = 'red'
    size = eq_data.get_magnitudes()

    return scatterplot.get_component(
        session_id, min_time, max_time, x_axis, y_axis, color, size
    )


@app.callback(
    Output('output-scatterplot', 'children'),
    [Input('session_id', 'children'),
     Input('time-frame', 'value'),
     Input('x-axis', 'value'),
     Input('y-axis', 'value'),
     Input('color', 'value'),
     Input('size', 'value')])
def update_output(session_id, time_frame, xaxis, yaxis, color, size):
    # TODO: Get these from user configuration
    min_time = datetime(2008, 1, 1, 0, 4)
    max_time = datetime(2008, 1, 9, 5)
    eq_data = earthquake_data.get_earthquake_data(session_id)
    x_axis = eq_data.get_datetimes()
    y_axis = eq_data.get_magnitudes()
    color = 'red'
    size = eq_data.get_depths()
    return scatterplot.update_output(
        session_id, min_time, max_time, x_axis, y_axis, color, size
    )
