import dash_core_components as dcc
import dash_html_components as html


def get_component(min_date, max_date, default_end_date, id="date-pick"):
    """Return the datepicker component.

    Keyword arguments:
    min_date -- The minimum date allowed to pick with the datepicker.
    max_date -- The maximum date allowed to pick with the datepicker.
    default_end_date -- The default end date for the datepicker. The
        default start date is the `min_date`.
    """
    start_date = None
    end_date = None

    if default_end_date is not None:
        start_date = min_date.date()
        end_date = default_end_date.date()

    return html.Div(children=[
        html.Div(className='config-label', children='Calendar'),
        dcc.DatePickerRange(
            id=id,
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=start_date,
            end_date=end_date,
            display_format='DD.MM.YYYY'
        )
    ])
