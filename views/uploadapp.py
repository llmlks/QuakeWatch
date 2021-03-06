import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from components import uploader
from components import instructions
from utils import session


def get_layout():
    """Return the layout for the upload page."""
    return dcc.Loading(html.Div([
        html.H2('QuakeWatch'),
        uploader.get_component(),
        instructions.get_component()
    ]))


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents'),
     Input('sample-dataset', 'n_clicks')],
    [State('upload-data', 'filename')])
def update_output(contents, clicks, filename):
    """Parse the given data and update the upload output.

    Keyword arguments:
    contents -- The contents of the uploaded data
    clicks -- Number of clicks on the sample dataset button
    filename -- The name of the uploaded file
    """
    if contents is None and clicks is None:
        raise PreventUpdate
    session_id = session.get_session_id()
    return uploader.update_output(
        contents, filename, session_id, clicks is not None
    )
