import dash_html_components as html
import dash_core_components as dcc


def get_component():
    """Return the instructions component."""
    with open('instructions.md') as f:
        return html.Div(
            dcc.Markdown(f.readlines())
        )
