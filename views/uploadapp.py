import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from components import uploader


layout = uploader.get_div()


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')])
def update_output(contents, filename):
    return uploader.update_output(contents, filename)
