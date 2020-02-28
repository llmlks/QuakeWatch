"""
Copyright 2018-2020 Faculty Science Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Code modified from https://github.com/facultyai/dash-bootstrap-components
"""
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app


page_names = ['Upload data', 'Map', 'Scatter plot']
page_paths = ['/upload', '/map', '/scatter']


def get_component():
    """Return the sidebar component."""
    return html.Div(
        [
            get_sidebar_header(),
            # use the Collapse component to animate hiding / revealing links
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavLink(
                            page_names[0],
                            href=page_paths[0],
                            id="page-0-link"),

                        dbc.NavLink(
                            page_names[1],
                            href=page_paths[1],
                            id="page-1-link"),

                        dbc.NavLink(
                            page_names[2],
                            href=page_paths[2],
                            id="page-2-link"),
                    ],
                    vertical=True,
                    pills=True,
                ),
                id="collapse",
            ),
        ],
        id="sidebar"
    )


def get_sidebar_header():
    """Return the sidebar header."""
    return dbc.Row(
        [
            dbc.Col(html.H2("QuakeWatch", className="display-5")),
            dbc.Col(
                [
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "borderColor": "rgba(0,0,0,.1)",
                        },
                        id="navbar-toggle",
                    ),
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "borderColor": "rgba(0,0,0,.1)",
                        },
                        id="sidebar-toggle",
                    ),
                ],
                # the column containing the toggle will be only as wide as the
                # toggle, resulting in the toggle being right aligned
                width="auto",
                # vertically align the toggle in the center
                align="center",
            ),
        ]
    )


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(len(page_paths))],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    """
    Return an array of booleans that describe which link is selected.

    The array contains one True value and n-1 False values where
    n is the number of links in the sidebar.
    """
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return [True, *[False for i in range(len(page_paths)-1)]]
    return [pathname == page_paths[i] for i in range(len(page_paths))]


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    """Return a class for the sidebar based on the toggle state."""
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    """Return True if the navbar should be collapsed, False otherwise."""
    return not is_open
