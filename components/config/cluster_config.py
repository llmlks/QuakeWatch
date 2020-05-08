import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from components.config import date_picker


def get_component(mindate, maxdate, session_id, id="1"):
    """Return the configuration component for the clustering view.
    that includesthe calendar, the input text box for the threshold
     value and the apply button

    Keyword arguments:
    mindate -- minimum date available for the data
    maxdate -- maximum date available
    session_id -- session-id used to track the session
    id -- id to differenciate between the two possible tabs in the app
    """
    id_component = "date-pick-{}".format(id)
    date_component = date_picker.get_component(
        mindate, maxdate, None, id_component)
    threshold_component = html.Div([
        dbc.Input(id="thr_{}".format(id), type="number",
                  value=1e-5, step=1e-5),
        dbc.Button('Apply', id='apply_thr_{}'.format(
            id), outline=True, color='success')
    ])
    return html.Div([
        html.Div(children=[
            date_component,
            html.Div(children="Threshold value:",
                     className="config-label"),
            threshold_component],
            title='Select the threshold value, which is used to determine the'
            ' maximum distance between earthquakes in one cluster'
        ),
        html.Div(
            id='intermediate-value',
            style={'display': 'none'},
            children=[session_id]
        ),
        dcc.Loading(
            id="loading-"+id,
            type="default",
            children=html.Div(id='output-clustering-'+id,
                              ))
    ])
