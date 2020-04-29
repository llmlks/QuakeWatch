import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import timedelta

from components import histogram
from components.config import histogram_config
from utils import earthquake_data
from app import app
from views.quake_map import get_datetime_from_str
from utils import session


def get_layout(session_id):
    """ Return the layout for a histogram and its configurations.

    Keyword arguments:
    session_id -- ID of the current session
    """
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is None or eq_data.data.shape == (0, 0):
        return 'No uploaded data found'

    start_date, end_date = eq_data.get_daterange()
    default_end_date = start_date + timedelta(weeks=1)
    filtered_data = eq_data.filter_by_dates(start_date, default_end_date)

    default_column = filtered_data.get_magnitudes()
    default_nbins = 10

    return html.Div([
            dbc.Col(
                html.Div(
                    id='histogram',
                    className='plot_sidebar_open',
                    children=histogram.get_component(
                        default_column, default_nbins)
                )
            ),
            dbc.Col(histogram_config.get_component(
                eq_data.data.columns, start_date, end_date,
                default_end_date, default_column.name))
    ])


@app.callback(
    Output('histogram', 'children'),
    [Input('apply', 'n_clicks')],
    [State('column', 'value'),
     State('nbins', 'value'),
     State('date-pick', 'start_date'),
     State('date-pick', 'end_date')])
def update_output(clicks, column, nbins, start_date, end_date):
    """ Return an updated histogram based on the changes in the configuration.

    Keyword arguments:
    clicks -- Number of clicks on the apply button
    session_id -- ID of the current session
    column -- Name of the column to use for the histogram
    start_date -- String from the date picker representing the start date
    end_date -- String from the date picker representing the end date
    """
    if clicks is None:
        raise PreventUpdate

    start_date = get_datetime_from_str(start_date)
    end_date = get_datetime_from_str(end_date) + timedelta(days=1)

    session_id = session.get_session_id()
    eq_data = earthquake_data.get_earthquake_data(session_id)
    filtered_data = eq_data.filter_by_dates(start_date, end_date)

    column = filtered_data.data[column]
    return histogram.get_component(column, nbins)


@app.callback(
    Output('histogram', 'className'),
    [Input('sidebar', 'className')])
def update_scatterplot_class(sidebar_class):
    """Return class name for div element containing a plot based
    on the collapsed state of the side bar.

    Keyword arguments:
    sidebar_class -- Current class name of the sidebar
    """

    if sidebar_class == '':
        return 'plot_sidebar_open'
    return 'plot_sidebar_collapsed'
