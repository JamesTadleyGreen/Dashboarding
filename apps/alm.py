import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import app




layout = html.Div(children=[
    dbc.Container(
        html.H4(children='ALM')
        , className="ml-2"
    ),
])