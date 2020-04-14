import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app
from utils import earthquake_data
from utils.dateutils import get_datetime_from_str
from components.config import date_picker
from components.config import timestep_picker
from components.config import template_picker
from components.config import size_picker
from components.config import color_picker
from components.config import faults_toggler


def get_component(min_date, max_date, default_end_date, columns,
                  show_faults, templates=None):
    """Return the configuration component for the map view.

    Keyword arguments:
    min_date -- The minimum date allowed to pick with the datepicker.
    max_date -- The maximum date allowed to pick with the datepicker.
    default_end_date -- The default end date for the datepicker. The
        default start date is the `min_date`.
    columns -- The available columns in the uploaded data
    show_faults -- Whether to display the faults toggler
    templates -- A list of template IDs to select from.
    """
    return html.Div([
        date_picker.get_component(min_date, max_date, default_end_date),
        timestep_picker.get_component(),
        size_picker.get_component(columns),
        color_picker.get_component(columns),
        template_picker.get_component(templates),
        faults_toggler.get_component(show_faults),
        dbc.Button("Apply", id='apply', outline=True,
                    color="success")
    ])


@app.callback(
    [Output('timestep-value', 'disabled'),
     Output('timestep-unit', 'disabled')],
    [Input('template-id', 'value')])
def toggle_time_configs_disabled(template_value):
    """Toggle the timestep value and unit selectors' disabled
    property according to whether a template ID has been selected.

    Keyword arguments:
    template_value -- Template ID selected by user
    """
    disabled = template_value is not None
    return (disabled, disabled)


@app.callback(
    Output('template-id', 'options'),
    [Input('date-pick', 'start_date'),
     Input('date-pick', 'end_date')],
    [State('session-id', 'children')])
def update_template_options(start_date, end_date, session_id):
    """Update the list of template IDs to choose from to include all template
    IDs occurring at least once in the selected time period.

    Keyword arguments:
    start_date -- String from the date picker representing the start date
    end_date -- String from the date picker representing the end date
    session_id -- ID of the current session
    """
    eq_data = earthquake_data.get_earthquake_data(session_id)

    start_date = get_datetime_from_str(start_date)
    end_date = get_datetime_from_str(end_date)

    templates = eq_data.filter_by_dates(start_date, end_date).get_templateids()
    if templates is None:
        templates = []

    return [{'label': template, 'value': template} for template in templates]
