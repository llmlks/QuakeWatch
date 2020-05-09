import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import timedelta

from components import heatmap
from components.config import heatmap_config
from utils import earthquake_data
from utils import session
from utils.dateutils import get_datetime_from_str
from app import app


def get_layout(session_id):
    """ Return the layout for a heatmap and its configurations.

    Keyword arguments:
    session_id -- ID of the current session
    """
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is None or eq_data.data.shape == (0, 0):
        return 'No uploaded data found'

    start_date, end_date = eq_data.get_daterange()
    filtered_data = eq_data.filter_by_dates(start_date, end_date)

    default_x = filtered_data.get_magnitudes()
    default_y = filtered_data.get_depths()

    default_nbins_x = 40
    default_nbins_y = 40

    z, xbins, ybins = filtered_data.get_weight_matrix(
        default_x.name, default_y.name, default_nbins_x, default_nbins_y
    )

    return html.Div([
        dbc.Row([
            dbc.Col(
                html.Div(
                    id='heatmap',
                    className='plot_sidebar_open',
                    children=heatmap.get_component(
                        z, xbins, ybins)
                )
            ),
            dbc.Col(heatmap_config.get_component(
                 start_date, end_date,
                 eq_data.data.select_dtypes(
                     include=['number', 'datetime']).columns,
                 default_x.name, default_y.name,
                 default_nbins_x, default_nbins_y))
        ])
    ])


@app.callback(
    Output('heatmap', 'children'),
    [Input('apply', 'n_clicks')],
    [State('x-axis', 'value'),
     State('y-axis', 'value'),
     State('date-pick', 'start_date'),
     State('date-pick', 'end_date'),
     State('nbins-x', 'value'),
     State('nbins-y', 'value')])
def update_output(clicks, x_axis, y_axis,
                  start_date, end_date, nbins_x, nbins_y):
    """ Return an updated heatmap based on the changes in the configuration.

    Keyword arguments:
    clicks -- Number of clicks on the apply button
    x-axis -- The column used for the x-axis
    y-axis -- The column used for the y-axis
    start_date -- String from the date picker representing the start date
    end_date -- String from the date picker representing the end date
    nbins_x -- Number of bins used for the x-axis
    nbins_y -- Number of bins used for the y-axis
    """
    if clicks is None:
        raise PreventUpdate

    start_date = get_datetime_from_str(start_date)
    end_date = get_datetime_from_str(end_date) + timedelta(days=1)

    session_id = session.get_session_id()
    eq_data = earthquake_data.get_earthquake_data(session_id)
    filtered_data = eq_data.filter_by_dates(start_date, end_date)

    x_axis = filtered_data.data[x_axis]
    y_axis = filtered_data.data[y_axis]

    z, xbins, ybins = filtered_data.get_weight_matrix(
        x_axis.name, y_axis.name, nbins_x, nbins_y
    )

    return heatmap.get_component(z, xbins, ybins)


@app.callback(
    Output('heatmap', 'className'),
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
