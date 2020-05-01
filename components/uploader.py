import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from utils import dataparser, earthquake_data


def get_component():
    """Return the uploader component."""
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
        dcc.Loading(
            children=html.Div(id='output-data-upload')
        )
    ])


def update_output(contents, filename, session_id):
    """Return a success or an error message depending on the success
    of parsing.

    Keyword arguments:
    contents -- The contents of the uploaded file as a binary string
    filename -- Name of the uploaded file
    session_id -- ID of the current session
    """

    if contents is not None:
        try:
            dataparser.parse_contents(contents, filename, session_id)
            eq_data = earthquake_data.get_earthquake_data(session_id)

            return dbc.Alert(
                """File {} uploaded successfully, {} rows. Please select a tool
                from the menu to inspect the data.
                """.format(filename, eq_data.data.shape[0]),
                color='success',
                className='alert-message'
            )

        except Exception as ex:
            print('Uploader:', ex)
            return html.Div([
                dbc.Alert(
                    'The file could not be parsed, please try another one',
                    color='danger',
                    className='alert-message'
                )
            ])
