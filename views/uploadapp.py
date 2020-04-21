import uuid

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import callback_context

from app import app
from components import uploader


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
    session_id = generate_session_id()
    return uploader.update_output(contents, filename, session_id)


def generate_session_id():
    """Generate a unique ID and set it as a cookie."""
    session_id = str(uuid.uuid4())
    callback_context.response.set_cookie(
       'quakewatch_session_id', session_id)
    return session_id
