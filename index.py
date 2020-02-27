import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from views import uploadapp
from components import sidebar


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar.get_component(),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """Display correct view based on the URL."""
    if pathname in ['/', '/upload']:
        return uploadapp.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
