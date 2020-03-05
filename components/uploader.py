import os

import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd

from utils import dataparser, earthquake_data


def get_table(session_id):
    """Fetch catalog data from cache and return it as a dash DataTable.

    Keywords arguments:
    session_id -- ID of the current session
    """
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is not None and eq_data.data.shape != (0, 0):
        return dash_table.DataTable(
            data=eq_data.data[:100].to_dict('records'),
            columns=[
                {'name': i, 'id': i} for i in eq_data.data.columns
            ],
            style_table={
                'overflow': 'auto',
                'width': '98%',
                'margin': '1%'
            }
        )


def get_component(session_id):
    """Return the uploader component.

    Keyword arguments:
    session_id -- ID of the current session
    """
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '95%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '2.5%'
            }
        ),
        html.Div(id='output-data-upload'),
    ])


def update_output(contents, filename, session_id):
    """Return an updated data table with uploaded data or an error
    message if parsing fails.

    Keyword arguments:
    contents -- The contents of the uploaded file as a binary string
    filename -- Name of the uploaded file
    """

    if contents is not None:
        try:
            dataparser.parse_contents(contents, filename, session_id)

            return get_table(session_id)

        except Exception as ex:
            print('Uploader:', ex)
            return html.Div([
                html.H5("""
                    The file could not be parsed, please try another one
                """),
            ])
