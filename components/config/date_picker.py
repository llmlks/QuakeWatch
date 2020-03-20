import dash_core_components as dcc
import dash_html_components as html


def get_component(min_date, max_date):
    return html.Div(children=[
        html.Div(className='config-label', children='Time range'),
        dcc.DatePickerRange(
            id='date-pick',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
        )
    ])
