from dash.dependencies import Input, Output

from components import scatterplot
from app import app


def get_layout(session_id):
    return scatterplot.get_component(session_id)


@app.callback(
    Output('output-scatterplot', 'children'),
    [Input('session_id', 'children')])
def update_output(session_id):
    return scatterplot.update_output(session_id)
