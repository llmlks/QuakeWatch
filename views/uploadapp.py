from dash.dependencies import Input, Output, State

from app import app
from components import uploader


def get_layout(session_id):
    return uploader.get_component(session_id)


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents'),
     Input('session-id', 'children')],
    [State('upload-data', 'filename')])
def update_output(contents, session_id, filename):
    return uploader.update_output(contents, filename, session_id)
