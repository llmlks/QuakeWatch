import numpy as np 
import pandas as pd 
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash
import dash_leaflet as dl

from app import app
import datetime 
from utils import earthquake_data
import math
from numba import njit, jit
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime as dt



def get_data( session_id ):
    eq_data = earthquake_data.get_earthquake_data(session_id)
    return eq_data
def compute_edges( df ):
    # add needed columns
    if df.empty: 
        return []
    #df['DateTime'] = df.apply(lambda x: get_datetime(x), axis = 1)
    #df["TimeStamp"] = df.DateTime.values.astype(np.int64) / 10 ** 9

    data = df[[ "TimeStamp" , "EVENTID" , "TimeStamp" , "MAGNITUDE" , "LATITUDE" , "LONGITUDE" ] ].values
    edges = compute_edges_numba( data )
    return edges


@jit( nopython=True )
def compute_edges_numba(  data  ):
    edges_numpy = np.zeros( (  len(data)  ,  3 )  )
    for i in range( len(data) ):
        
        timestamp = data[i][0]
        
        data2 = data[ data[: , 0]  < timestamp ]
        if len( data2 ) == 0:
            continue 
        time_diff = timestamp - data2[: , 0]
        dist = np.zeros( ( len(data2) ) )
        for k in range( len(data2) ):
            d = (data[i][4] - data2[k][ 4])**2  +  (data[i][5] - data2[k][5] )**2
            dist[k] = d
        dist = np.sqrt( dist )
        x = time_diff*dist**(1.6)*(10**( -data[i][3] ))
        #dists = [  geopy.distance.distance( ( data[i][4] , data[i][5]  ) , (  data2[k][ 4] , data2[k][5]   )  ).km for k in range(len(data2))  ] 
        #x = time_diff*dist**(1.6)*(10**( -data[i][3] ))
        indx = np.argmin( x )
        #edges.append( ( data2[indx][1] ,   data2[i][1]  , { "w" : x[indx ] }   )  )
        edges_numpy[i][0] = data2[indx][1]
        edges_numpy[i][1] = data[i][1] 
        edges_numpy[i][2] = x[ indx ]
    return edges_numpy


def get_component( session_id ):
    data = get_data(session_id)

    #edges = compute_edges( data.data )
    mindate , maxdate = data.get_daterange()
    items = []
    items.append( html.H1("Clustering" ) )
    items.append( html.H3("Select a date range"))
    items.append( 

    html.Div([
    dcc.DatePickerRange(
        id='date-pick',
        min_date_allowed=mindate,
        max_date_allowed=maxdate,
    ),
    html.Div(id='intermediate-value', style={'display': 'none'} , children = [session_id
    ] )  , 
    html.Div(id='output-container-date-picker-range')
])


    )
    return html.Div( items )

@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('date-pick', 'start_date'),
     dash.dependencies.Input('date-pick', 'end_date') , 
     dash.dependencies.Input('session-id' , "children")
      ]  )
def update_output(start_date, end_date , session_id ):
    
    if start_date is None or end_date is None :
        return "No Falafel for you"
    
    print( start_date , end_date)
    data = get_data(session_id)
    df = data.get_data_by_daterange( start_date , end_date )

    edges = compute_edges( df )
    if edges == []: 

        figures = [ go.Figure() ]
    else:
        figures = get_figures( edges , data.data ) 

    graphs = [ ]
    for  i , fig in  enumerate( figures ) :
        graphs.append( dcc.Graph( id = "fig-{}".format(i) ,  figure = fig  ) )

    return graphs 


def get_figures( edges_np , df  ):

    edges = [] 
    for e in edges_np[1:]:
        
        edges.append(  (  e[0]  , e[1]    ,  { "w" : e[2]}  ))

    G=nx.DiGraph()
    G.add_edges_from( edges )

    th = 1e3
    to_remove = [ ]
    for e in G.edges:
        #print( e )
        w = G.edges[ e ]["w"]
        #print( 1.0/w )
        if w  >= th :
            print("remove")
            to_remove.append( ( e[0]  , e[1]   )   )
    G.remove_edges_from( to_remove )
    position_dict = compute_pos( df , G.nodes() )

    UG = G.to_undirected()
    # extract subgraph
    sub_graphs = [ UG.subgraph(c) for c in nx.connected_components(UG) ]

    figures = get_plots( sub_graphs , position_dict ) 
    return figures 
def compute_pos( df, nodes ):
    ##
    pos = {}
    for n in nodes:
        #print(n)
        row = df[ df["EVENTID"] == int( n )   ]
        #print( int( n ) )
        #print( row ) 
        x = str( row[ "DateTime"].values[0] )  
        y =  row["MAGNITUDE"].values[0] 
        
        pos[n] = ( x, y )
        
    return pos

def get_plots( graphs , positions  ):
    plots = []
    for g in graphs:
        fig = get_plot( g , positions )
        plots.append( fig )
    return plots 

def get_plot( graph , positions ):
    # build plotly figure 

    Xe = [ ]
    Ye = [ ]
    for n in graph:
        Xe.append( str( positions[n][0] ) )
        Ye.append( positions[n][1] )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                    y=Ye,
                    mode='lines',
                    line=dict(color='rgb(210,210,210)', width=3),
                    hoverinfo='none' , name = ""
                    ))

    fig.add_trace(go.Scatter(x=Xe,
                    y=Ye,
                    mode='markers',
                    name='Earthquake',
                    marker=dict(symbol='circle-dot',
                                    size=18,
                                    color='#6175c1',    #'#DB4551',
                                    line=dict(color='rgb(50,50,50)', width=1)
                                    )
                    ))

    return fig

