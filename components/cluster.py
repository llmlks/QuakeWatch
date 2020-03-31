import datetime
import math
from datetime import datetime as dt

import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash
import dash_leaflet as dl
from numba import njit, jit
import networkx as nx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from app import app
from utils import earthquake_data
from components.config import date_picker


def get_data(session_id):
    eq_data = earthquake_data.get_earthquake_data(session_id)
    return eq_data


def compute_edges(data):
    """Return the list of edges to be used to build the clustering graph.

    Keyword arguments:
    data -- numpy array holding the data (columns specified in compute_edges)
    """
    # the data representation somehow deattach the dates and the data and
    # in order to work the algothim need all the information in one array
    # a bit of mannuvering was required to get the data together in an array
    # and later a dataframe that is used to compute the positions
    mag = data.get_magnitudes().values
    lat = data.get_latitudes().values
    lon = data.get_longitudes().values
    ids = data.get_eventids().values
    dates = data.get_datetimes()

    vals = np.zeros((5, len(dates)))
    vals[0, :] = dates
    vals[1, :] = ids
    vals[2, :] = mag
    vals[3, :] = lat
    vals[4, :] = lon
    vals = vals.T

    new_df = pd.DataFrame(vals)
    new_df.columns = ["DateTime", "EVENTID",
                      "MAGNITUDE", "LATITUDE", "LONGITUDE"]

    edges = compute_edges_numba(vals)
    return edges, new_df


@jit(nopython=True)
def compute_edges_numba(data):
    """Return the list of edges to be used to build the clustering graph.
    The edges are computed used numba compiler for infinite power

    Keyword arguments:
    data -- numpy array holding the data (columns specified in compute_edges)
    """
    edges_numpy = np.zeros((len(data), 3))
    for i in range(len(data)):
        timestamp = data[i][0]
        data2 = data[data[:, 0] < timestamp]
        if len(data2) == 0:

            continue
        time_diff = timestamp - data2[:, 0]
        dist = np.zeros((len(data2)))
        for k in range(len(data2)):
            d = (data[i][3] - data2[k][3])**2 + (data[i][4] - data2[k][4])**2
            dist[k] = d
        dist = np.sqrt(dist)
        x = time_diff*dist**(1.6)*(10**(-data[i][2]))
        indx = np.argmin(x)
        edges_numpy[i][0] = data2[indx][1]
        edges_numpy[i][1] = data[i][1]
        edges_numpy[i][2] = x[indx]
    return edges_numpy


def get_component(session_id):
    """Return the main component of the cluster view.
    The component is composed by a header, a datepicker and a placeholder

    Keyword arguments:

    session_id -- string with the session_id
   """
    data = get_data(session_id)
    mindate, maxdate = data.get_daterange()
    if maxdate - mindate <= datetime.timedelta(days=1):
        maxdate = maxdate + datetime.timedelta(days=1)
    items = []
    items.append(html.H1("Clustering"))
    items.append(html.H4("Compare clusters"))
    tab1 = build_cluster_component(mindate, maxdate, session_id, "1")
    tab2 = build_cluster_component(mindate, maxdate, session_id, "2")
    items.append(
        dcc.Tabs([
            dcc.Tab(label='Date 1', children=[tab1]),
            dcc.Tab(label="Date 2", children=[tab2])

        ])
    )
    return html.Div(items)


def build_cluster_component(mindate, maxdate, session_id, idd="1"):
    id_component = "date-pick-{}".format(idd)
    date_component = date_picker.get_component(
        mindate, maxdate, mindate + datetime.timedelta(days=1), id_component)
    return html.Div([
        date_component,
        html.Div(
            id='intermediate-value',
            style={'display': 'none'},
            children=[session_id]
        ),

        html.Div(id='output-clustering-'+idd)

    ])


@app.callback(
    Output('output-clustering-1', 'children'),
    [
        Input('date-pick-1', 'start_date'),
        Input('date-pick-1', 'end_date'),
        Input('session-id', "children")
    ])
def update_output(start_date, end_date, session_id):
    """Return the list of graphs.This is a callback function

    Keyword arguments:

    start_date -- datetime, from the calendar component
    end_date -- datetime , from the calendar component
   """
    if start_date is None or end_date is None:
        return "No Data"
    print("Computing clusters...")
    start_date = dt.strptime(start_date,  "%Y-%m-%d")
    end_date = dt.strptime(end_date,  "%Y-%m-%d")

    data = get_data(session_id)
    data = data.filter_by_dates(start_date, end_date)

    df = data.data
    if df.empty:
        figures = [go.Figure()]
    else:
        edges, df = compute_edges(data)
        figures = get_figures(edges, df)

    graphs = []
    for i, fig in enumerate(figures):
        c = dcc.Graph(id="fig-{}".format(i),  figure=fig)
        graphs.append(c)
    print("Done!")
    return graphs


@app.callback(
    Output('output-clustering-2', 'children'),
    [
        Input('date-pick-2', 'start_date'),
        Input('date-pick-2', 'end_date'),
        Input('session-id', "children")
    ])
def update_output(start_date, end_date, session_id):
    """Return the list of graphs.This is a callback function

    Keyword arguments:

    start_date -- datetime, from the calendar component
    end_date -- datetime , from the calendar component
   """
    if start_date is None or end_date is None:
        return "No Data"
    print("Computing clusters...")
    start_date = dt.strptime(start_date,  "%Y-%m-%d")
    end_date = dt.strptime(end_date,  "%Y-%m-%d")

    data = get_data(session_id)
    data = data.filter_by_dates(start_date, end_date)

    df = data.data
    if df.empty:
        figures = [go.Figure()]
    else:
        edges, df = compute_edges(data)
        figures = get_figures(edges, df)

    graphs = []
    for i, fig in enumerate(figures):
        graphs.append(dcc.Graph(id="fig-{}".format(i),  figure=fig))
    print("Done!")
    return graphs


def get_figures(edges_np, df):
    """Return list of plotly figures. One figure per cluster

    Keyword arguments:

    edges_np -- numpy, result from the numba computation
    df -- datetime , dataframe with the catalog
   """
    edges = []
    for e in edges_np[1:]:
        edges.append((e[0], e[1],  {"w": e[2]}))

    G = nx.DiGraph()
    G.add_edges_from(edges)
    # this threshold value is experimental and subject to changes.
    th = 1e-5
    to_remove = []
    # this loop will remove the weak edges. weak edges are the ones
    # with a distance above the threshold  defined above as th.
    for e in G.edges:
        w = G.edges[e]["w"]
        if 1.0/w >= th:
            to_remove.append((e[0], e[1]))
    G.remove_edges_from(to_remove)
    position_dict = compute_pos(df, G.nodes())

    UG = G.to_undirected()
    # extract the list of disjoint subgraphs
    sub_graphs = [UG.subgraph(c) for c in nx.connected_components(UG)]

    sub_graphs = [(g, len(g)) for g in sub_graphs]
    sub_graphs = sorted_by_second = sorted(
        sub_graphs, key=lambda tup: tup[1], reverse=True)
    sub_graphs = [x[0] for x in sub_graphs]

    figures = get_plots(sub_graphs, position_dict)
    return figures


def compute_pos(df, nodes):
    """Return a dictionary with the nodes as keys and the coordinates to
    be plotted as values

    Keyword arguments:

    df -- dataframe, the catalog
    nodes -- list of nodes, result from G.nodes() with G being the networkx
    graph constructed out of the edges computed.
   """
    pos = {}
    for n in nodes:
        row = df[df["EVENTID"] == int(n)]
        x = row["DateTime"].values[0]
        x = dt.fromtimestamp(x//10**9)
        y = row["MAGNITUDE"].values[0]
        lat = row["LATITUDE"].values[0]
        lon = row["LONGITUDE"].values[0]
        pos[n] = (x, y, lat, lon)
    return pos


def get_plots(graphs, positions):
    """Return list of plotly figures.

    Keyword arguments:

    graphs -- list, list of disjoint graphs
    positions -- dict, result from compute_pos
   """
    plots = []
    for g in graphs:
        fig = get_plot(g, positions)
        plots.append(fig)
    return plots


def get_plot(graph, positions):
    """Return plotly figure for a single graph

    Keyword arguments:

    graph -- Networkx graph, list of disjoint graphs
    positions -- dict, result from compute_pos
   """
    Xe = []
    Ye = []

    X_foreshocks = []
    Y_foreshocks = []
    Hover_foreshocks = []

    X_aftershocks = []
    Y_aftershocks = []
    Hover_aftershocks = []

    max_magnitude = -1000
    max_time = 0.0
    hovermainshock = 0, 0
    for n in graph:
        mag = positions[n][1]
        Xe.append(positions[n][0])
        Ye.append(positions[n][1])

        if mag >= max_magnitude:
            max_magnitude = mag
            max_time = positions[n][0]
            hovermainshock = "Location:({},{})".format(
                positions[n][2], positions[n][3])

    for n in graph:
        mag = positions[n][1]
        if mag == max_magnitude:
            # cont
            continue
        text = "Location:({},{})".format(positions[n][2], positions[n][3])
        if positions[n][0] < max_time:
            # foreshock
            X_foreshocks.append(positions[n][0])
            Y_foreshocks.append(positions[n][1])
            Hover_foreshocks.append(text)
        else:
            # aftershocks
            X_aftershocks.append(positions[n][0])
            Y_aftershocks.append(positions[n][1])
            Hover_aftershocks.append(text)
        # Xe.append(positions[n][0]  )
        # Ye.append(positions[n][1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=Xe,
        y=Ye,
        mode='lines',
        line=dict(color='rgb(210,210,210)', width=3),
        hoverinfo='none', name=""
    ))
    fig.add_trace(get_figure(X_foreshocks, Y_foreshocks,
                             Hover_foreshocks, "Foreshocks", '#ffe100'))
    fig.add_trace(get_figure(X_aftershocks, Y_aftershocks,
                             Hover_aftershocks, "Aftershocks", '#0d35a5'))
    fig.add_trace(get_figure([max_time], [max_magnitude], [
                  hovermainshock], "Mainshock", '#ba0000'))

    return fig

# '#0055ff' aftershocks
# '#ba0000' mainshock
#  '#0055ff' foreshocks


def get_figure(x, y, hovertext, name, color):
    """Return a plotly figure given the x,y and hover information

    Keyword arguments:

    x -- list x-coordinate
    y -- list y-coordinate
    name -- string  name to be displayed
    color -- string hexcolor code
    """
    return go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name=name,
        hovertext=hovertext,
        hoverinfo="text",
        marker=dict(
            symbol='circle-dot',
            size=18,
            color=color,
            line=dict(color='rgb(50,50,50)', width=1)
        )
    )
