from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from components import uploader
from utils import session


def get_layout(session_id):
    """Return the upload component."""
    return uploader.get_component(session_id)


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')])
def update_output(contents, filename):
    """Parse the given data and update the upload output.

    Also generate a session ID and set it as a cookie
    so that the uploaded data is accessible during the session.

    Keyword arguments:
    contents -- The contents of the uploaded data
    filename -- The name of the uploaded file
    """
    if contents is None:
        raise PreventUpdate
    session_id = session.get_session_id()
    return uploader.update_output(contents, filename, session_id)
