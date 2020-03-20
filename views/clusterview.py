from dash.dependencies import Input, Output, State

from app import app
from components import uploader
from components import cluster


def get_layout(session_id):

    return cluster.get_component(session_id)
