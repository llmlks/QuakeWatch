import numpy as np 
import pandas as pd 
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import dash_leaflet as dl

from app import app
import datetime 
from utils import earthquake_data
import math
from numba import njit, jit
import plotly.graph_objects as go
import networkx as nx

def get_datetime(x):
    millisec, second = math.modf(x.SECOND)
    microsec = millisec * 1000000
    minute = x.MINUTE
    if minute >= 60:
        minute = 59
    if second >=60 :
        second = 59
    return datetime.datetime(int(x.YEAR), int(x.MONTH), int(x.DAY), int(x.HOUR), int(minute), int(second), int(microsec))

def get_data( session_id ):
    eq_data = earthquake_data.get_earthquake_data(session_id)
    return eq_data
def compute_edges( df ):
    # add needed columns
    if df.empty: 
        return []
    df['DateTime'] = df.apply(lambda x: get_datetime(x), axis = 1)
    df["TimeStamp"] = df.DateTime.values.astype(np.int64) / 10 ** 9

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
    edges = compute_edges( data.data )
    if edges == []: 

        figures = [ go.Figure() ]
    else:
        figures = get_figures( edges , data.data ) 

    items = []
    items.append( html.H1("Clustering" ) )

    for  i , fig in  enumerate( figures ) :
        items.append( dcc.Graph( id = "fig-{}".format(i) ,  figure = fig  )  )
    
    return html.Div( items )

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

