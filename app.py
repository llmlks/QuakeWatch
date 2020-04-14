import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
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
