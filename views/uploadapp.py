import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from components import uploader
from components import instructions
from utils import session


def get_layout(session_id):
    """Return the layout for the upload page."""
    return html.Div([
        instructions.get_component(),
        uploader.get_component(session_id)
    ])


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')])
def update_output(contents, filename):
    """Parse the given data and update the upload output.

    Keyword arguments:
    contents -- The contents of the uploaded data
    filename -- The name of the uploaded file
    """
    if contents is None:
        raise PreventUpdate
    session_id = session.get_session_id()
    return uploader.update_output(contents, filename, session_id)
