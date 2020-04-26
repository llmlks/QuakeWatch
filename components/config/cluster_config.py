import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


def get_component(id="1"):

    idd = "thr_{}".format(id)
    return html.Div([
        dcc.Input(id=idd, type="number",  value=1e-5),
        dbc.Button('Apply', id='apply_thr_{}'.format(
            id), outline=True, color='success')
    ])
