import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import callback_context
from flask import request

from app import app, server
from views import uploadapp
from views import quake_map
from views import clusterview
from views import scatterplot

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
    session_id = request.cookies.get('quakewatch_session_id')
    if pathname in ['/', '/upload']:
        return uploadapp.get_layout(session_id)
    if pathname == '/map':
        return quake_map.get_layout(session_id)
    if pathname == '/cluster':
        return clusterview.get_layout(session_id)
    if pathname == '/scatter':
        return scatterplot.get_layout(session_id)

    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
