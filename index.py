import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from views import uploadapp
from views import quake_map
from views import clusterview
from views import scatterplot
<<<<<<< HEAD
from views import histogram
=======
from views import dataview
from utils import session
>>>>>>> master

from components import sidebar


def get_layout():
    """Return page content."""
    return html.Div([
        dcc.Location(id='url', refresh=False),
        sidebar.get_component(),
        html.Div(id='page-content')
    ])


app.layout = get_layout()


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """Display correct view based on the URL.

    Keyword arguments:
    pathname -- The current URL ending
    """
    session_id = session.get_session_id()
    if session_id is None:
        session_id = session.generate_session_id()

    if pathname in ['/', '/upload']:
        return uploadapp.get_layout()
    if pathname == '/map':
        return quake_map.get_layout(session_id)
    if pathname == '/cluster':
        return clusterview.get_layout(session_id)
    if pathname == '/scatter':
        return scatterplot.get_layout(session_id)
<<<<<<< HEAD
    if pathname == '/histogram':
        return histogram.get_layout(session_id)
=======
    if pathname == '/data':
        return dataview.get_layout(session_id)
>>>>>>> master

    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
