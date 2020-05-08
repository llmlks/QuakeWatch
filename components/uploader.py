import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from utils import dataparser, earthquake_data
from app import app

SAMPLE_DATA_FILENAME = 'sc2018_hash_ABCD_so.focmec.scedc'


def get_component():
    """Return the uploader component."""
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ])
        ),
        html.Div([
            html.Div(
                dbc.Button(
                    'Use sample catalog', color='primary'
                ),
                id='sample-dataset',
                title='Use the sample SCEDC 2018 Focal Mechanism catalog'
            ),
            dcc.Loading(
                id='output-data-upload',
                className='alert-message'
            )
        ], id='output-container')
    ])


def update_output(contents, filename, session_id, use_sample_data=False):
    """Return a success or an error message depending on the success
    of parsing.

    Keyword arguments:
    contents -- The contents of the uploaded file as a binary string
    filename -- Name of the uploaded file
    session_id -- ID of the current session
    use_sample_data -- Whether the sample data set should be used
    """
    if use_sample_data:
        filename = SAMPLE_DATA_FILENAME

    if contents is not None or use_sample_data:
        try:
            dataparser.parse_contents(
                contents, filename, session_id, use_sample_data
            )
            eq_data = earthquake_data.get_earthquake_data(session_id)

            return dbc.Alert(
                """File {} uploaded successfully, {} rows. Please select a tool
                from the menu to inspect the data.
                """.format(filename, eq_data.data.shape[0]),
                color='success'
            )

        except Exception as ex:
            print('Uploader:', ex)
            return html.Div([
                dbc.Alert(
                    'The file could not be parsed, please try another one',
                    color='danger'
                )
            ])
