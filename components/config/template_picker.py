import dash_core_components as dcc
import dash_html_components as html


def get_component(templates):
    """Return a template picker component.

    If the templates list is None, the component is not visible.

    Keyword arguments:
    templates -- A list of template IDs to select from
    """
    display_style = {}

    if templates is None:
        templates = []
        display_style = {'display': 'none'}

    return html.Div([
        html.Div(className='config-label', children='Template ID'),
        dcc.Dropdown(
            id='template-id',
            clearable=True,
            searchable=True,
            options=[
              {'label': template, 'value': template}
              for template in templates
            ],
            value=None
        )
    ], style=display_style)
