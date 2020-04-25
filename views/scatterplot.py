from datetime import timedelta

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from components import scatterplot
from components.config import scatterplot_config
from components.config.size_picker import get_sizes
from utils import earthquake_data
from utils.catalog_types import CatalogTypes
from views.quake_map import get_datetime_from_str
from app import app
from utils import session


def get_layout(session_id):
    """Return the layout for a scatter plot and its configurations.

    Keyword arguments:
    session_id -- ID of the current session
    """
    eq_data = earthquake_data.get_earthquake_data(session_id)

    if eq_data is None or eq_data.data.shape == (0, 0):
        return 'No uploaded data found'

    start_date, end_date = eq_data.get_daterange()
    default_end_date = start_date + timedelta(weeks=1)
    filtered_data = eq_data.filter_by_dates(start_date, default_end_date)

    x_axis = filtered_data.get_datetimes()
    y_axis = filtered_data.get_depths()
    if CatalogTypes(filtered_data.catalog_type) == CatalogTypes.CSV_EXT:
        y_axis = -y_axis

    color = 'red'
    default_size_column = eq_data.get_column_params(
        eq_data.get_magnitudes().name
    )
    sizes = get_sizes(
        filtered_data.data,
        default_size_column,
        is_map=False
    )

    return html.Div([
        dbc.Row([
            dbc.Col(
                html.Div(
                    id='scatter-plot',
                    className='plot_sidebar_open',
                    children=scatterplot.get_component(
                        x_axis, y_axis, color, sizes
                    )
                )
            ),
            dbc.Col(scatterplot_config.get_component(
                start_date, end_date, default_end_date,
                filtered_data.data.columns,
                filtered_data.data.select_dtypes(
                    include='number'
                ),
                x_axis.name, y_axis.name,
                default_size_column[0]
            ))
        ])
    ])


@app.callback(
    Output('scatter-plot', 'children'),
    [Input('apply', 'n_clicks')],
    [State('date-pick', 'start_date'),
     State('date-pick', 'end_date'),
     State('x-axis', 'value'),
     State('y-axis', 'value'),
     State('size-column', 'value'),
     State('color-column', 'value')])
def update_output(clicks, start_date, end_date, x_axis, y_axis,
                  size_column, color_column):
    """Return an updated scatter plot based on changes in the configuration.

    Keyword arguments:
    clicks -- Number of clicks on the apply button
    start_date -- String from the date picker representing the start date
    end_date -- String from the date picker representing the end date
    x_axis -- Name of the column to use for x-axis
    y_axis -- Name of the column to use for y-axis
    size_column -- The column for computing the size of each data point
    color_column -- The column for computing the color of each data point
    """
    if clicks is None:
        raise PreventUpdate

    start_date = get_datetime_from_str(start_date)
    end_date = get_datetime_from_str(end_date)

    session_id = session.get_session_id()
    eq_data = earthquake_data.get_earthquake_data(session_id)
    filtered_data = eq_data.filter_by_dates(start_date, end_date)

    sizes = get_sizes(
        filtered_data.data,
        eq_data.get_column_params(size_column),
        False
    )

    if color_column is None:
        colors = 'red'
    else:
        colors = filtered_data.data[color_column]

    x_axis = filtered_data.data[x_axis]
    y_axis = filtered_data.data[y_axis]

    return scatterplot.get_component(
        x_axis, y_axis, colors, sizes
    )


@app.callback(
    Output('scatter-plot', 'className'),
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
