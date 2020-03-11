import dash_html_components as html
import dash_core_components as dcc

from utils import earthquake_data


def get_graph(session_id):
    """Return an empty scatterplot graph, if data has been uploaded.
    Otherwise returns a text informing the user, that no data was found.

    Keywords arguments:
    session_id -- ID of the current session
    """
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is not None and eq_data.data.shape != (0, 0):
        df = eq_data.data
        return dcc.Graph()
    return html.Div(["Uploaded data not found."], id='output-scatterplot')


def get_component(session_id):
    """
    Return the scatterplot component.

    Keyword arguments:
    session_id -- ID of the current session
    """
    return html.Div([
        get_graph(session_id)
    ])


def update_output(session_id):
    return get_graph(session_id)
