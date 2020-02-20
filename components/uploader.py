import dash_html_components as html
import dash_core_components as dcc
import dash_table
from utils import dataparser


def get_div():
    """
    Return the uploader component
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


def update_output(contents, filename):
    """
    Update the data table on the page, or display error
    message if parsing fails.
    """

    if contents is not None:
        try:
            data = dataparser.parse_contents(contents, filename)
            return html.Div([
                html.H5(filename),

                dash_table.DataTable(
                    data=data[:20].to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in data.columns]
                ),

                html.Hr()
            ])
        except Exception:
            return html.Div([
                html.H5("""
                    The file could not be parsed, please try another one
                """),
            ])
