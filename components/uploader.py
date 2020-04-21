import dash_html_components as html
import dash_core_components as dcc

from utils import dataparser, earthquake_data


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
    """Redirect to data view or return an error message if parsing fails.

    Keyword arguments:
    contents -- The contents of the uploaded file as a binary string
    filename -- Name of the uploaded file
    """

    if contents is not None:
        try:
            dataparser.parse_contents(contents, filename, session_id)

            return dcc.Location(pathname='/data', id='redirect-after-upload')

        except Exception as ex:
            print('Uploader:', ex)
            return html.Div([
                html.H5("""
                    The file could not be parsed, please try another one
                """),
            ])
