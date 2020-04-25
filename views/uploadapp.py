import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from components import uploader
from components import instructions


def get_layout(session_id):
    """Return the layout for the upload page."""
    return html.Div([
        html.H2('QuakeWatch'),
        uploader.get_component(session_id),
        instructions.get_component()
    ])


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents'),
     Input('session-id', 'children')],
    [State('upload-data', 'filename')])
def update_output(contents, session_id, filename):
    return uploader.update_output(contents, filename, session_id)
