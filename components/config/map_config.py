import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from components.config import date_picker
from components.config import timestep_picker
from components.config import template_picker


def get_component(min_date, max_date, default_end_date, templates=None):
    """Return the configuration component for the map view.

    Keyword arguments:
    min_date -- The minimum date allowed to pick with the datepicker.
    max_date -- The maximum date allowed to pick with the datepicker.
    default_end_date -- The default end date for the datepicker. The
        default start date is the `min_date`.
    templates -- A list of template IDs to select from.
    """
    return html.Div([
        date_picker.get_component(min_date, max_date, default_end_date),
        timestep_picker.get_component(),
        template_picker.get_component(templates),
        dbc.Button("Apply", id='apply', outline=True, color="success")
    ])
