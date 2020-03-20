import dash_core_components as dcc


def get_component(min_date, max_date):
    return dcc.DatePickerRange(
        id='date-pick',
        min_date_allowed=min_date,
        max_date_allowed=max_date,
    )
