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

app.config.suppress_callback_exceptions = True

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '.cache-directory',

    # Maximum number of concurrent users. Modifiable
    'CACHE_THRESHOLD': 50
})
