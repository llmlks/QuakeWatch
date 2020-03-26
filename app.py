import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
server = app.server

server.config.from_object("config")
app.config.suppress_callback_exceptions = True

cache = Cache(server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '.cache-directory',

    # Maximum number of concurrent users. Modifiable
    'CACHE_THRESHOLD': 50
})
