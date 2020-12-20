import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import app

# Colour Scheme -------------------------------------------------------
pwc_colours = {'red': '#AD1B02','dark orange': '#D85604','orange': '#E88D14','yellow': '#F3BE26','pink': '#E669A2'}
website_colors = {'grey': '#7E7E7E', 'light grey': '#d3d3d3', 'dark grey': '#333333'}
scenario_dict = {0: 'Upside', 1: 'Base', 2: 'Downside', 3: 'Severe Downside'}

# DATA LOAD --------------------------------------------------------
ALM_df = pd.read_csv("./Data/ALM.csv")

# NAME DICTS --------------------------------------------------------
portfolio_name_dict = {0: 'Simple Investment Strategy', 1: 'Credit Investment Strategy', 2: 'Agressive investment Strategy'}
ALM_name_dict = {0: 'BO Base', 1: 'BO Downside'}

# GRAPH FUNCTS --------------------------------------------------------
def ALM_filter(data, portfolio, basis):
    fig = go.Figure()
    for q in data['Quantile'].unique():
        fig.add_trace(go.Scatter(
            x = data['Year'].unique(),
            y = data[(data['Portfolio Basis']==portfolio) & (data['ALM Basis']==basis) & (data['Quantile']==q)]['Value'].to_list(),
            mode='lines+markers',
            name=scenario_dict[q],
            line=dict(color=list(pwc_colours.values())[q], width=2),
        ))
    
    fig.update_layout(
            showlegend = True,
            template = 'plotly_white',
    )
    return fig

# TEXT ------------------------------------------------------------
alm_text = [f'''
### Observations
---
* We see that for the upside scenario at year 20 we have a funding level of {ALM_df[(ALM_df['Portfolio Basis']==0) & (ALM_df['ALM Basis']==0) & (ALM_df['Quantile']==0) & (ALM_df['Year']==20)]['Value'].values*100}%.
* The volitility of the strategy means that we get above average returns.
* asd
''',
    f'''### Notes

    We see an upper value of % and a lower value of %.
    ''',
]

# APP LAYOUT ------------------------------------------------------
# HEADER ----------------------------------------------------------
layout_header = html.Div(children=[
    dbc.Container(
        html.H4(children='ALM'), className="ml-2"
    ),
])

# BODY ------------------------------------------------------------
layout = html.Div(children=[
    # Graphs
    html.Hr(style={"height": "3px", "border": "none", "background-color": website_colors['light grey']}), 
    
    dbc.Container(fluid=True, children=
        [
            dbc.Col(children =
                [
                    dcc.Graph(
                        style={'height': '70vh'},
                        id='alm-graph',
                        config={'displayModeBar': False},
                    ),
                    dcc.Markdown(alm_text[0])
                ]
            )
        ]
    )
])

# APP CALLBACKS ------------------------------------------------------
@app.callback(
    Output('alm-graph', 'figure'),
    [
    Input('portfolio-select', 'value'), 
    Input('ALM-select', 'value'),]
)
def update_graph(portfolio, basis):
    return ALM_filter(ALM_df, portfolio, basis)