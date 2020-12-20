import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Name Dictionaries
portfolio_name_dict = {0: 'Simple Investment Strategy', 1: 'Credit Investment Strategy', 2: 'Agressive investment Strategy'}
ALM_name_dict = {0: 'BO Base', 1: 'BO Downside'}
scenario_dict = {0: 'Upside', 1: 'Base', 2: 'Downside', 3: 'Severe Downside'}

# SLICERS -----------
slicers = [
    dbc.Container(fluid=True,children=
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label('Year: 7', id='year-slicer-header'),
                            dcc.Slider(
                            id='year-select',
                            min=1,
                            max=20,
                            marks = {1: '1', 20: '20'},
                            value=7,
                            included=False
                            )
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label('Portfolio:', id='portfolio-slicer-header'),
                            dcc.Dropdown(
                            id='portfolio-select',
                            options=[
                                {'label': portfolio_name_dict[0], 'value': 0},
                                {'label': portfolio_name_dict[1], 'value': 1},
                                {'label': portfolio_name_dict[2], 'value': 2},
                            ],
                            value=0,
                            searchable=False,
                            clearable=False,
                            )
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label('ALM Basis:', id='ALM-slicer-header'),
                            dcc.Dropdown(
                            id='ALM-select',
                            options=[
                                {'label': ALM_name_dict[0], 'value': 0},
                                {'label': ALM_name_dict[1], 'value': 1},
                            ],
                            value=0,
                            searchable=False,
                            clearable=False,
                            )
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label('Scenario:', id='quantile-slicer-header'),
                            dcc.Dropdown(
                            id='quantile-select',
                            options=[
                                {'label': scenario_dict[0], 'value': 0},
                                {'label': scenario_dict[1], 'value': 1},
                                {'label': scenario_dict[2], 'value': 2},
                                {'label': scenario_dict[3], 'value': 3},
                            ],
                            value=1,
                            searchable=False,
                            clearable=False,
                            )
                        ],
                    ),
                ],
            ),
        ]
    ),]