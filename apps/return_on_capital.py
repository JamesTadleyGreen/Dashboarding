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

# DATA LOAD --------------------------------------------------------
waterfall_df = pd.read_csv("./Data/Waterfall.csv")

# NAME DICTS --------------------------------------------------------
portfolio_name_dict = {0: 'Simple Investment Strategy', 1: 'Credit Investment Strategy', 2: 'Agressive investment Strategy'}
ALM_name_dict = {0: 'BO Base', 1: 'BO Downside'}
waterfall_name_dict = {0: 'Premium TP', 1: 'Unwinding of Buyout', 2: 'Return of Buyout', 3: 'Capital Buffer', 4: 'Replayment of Capital', 5: 'Benefits Paid', 6: 'Return on Capital in'}


# GRAPH FUNCTS --------------------------------------------------------
def waterfall_filter(data, year, portfolio, basis, scenario):
    fig = go.Figure(go.Waterfall(
            measure = ["relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x = list(waterfall_name_dict.values()),
            textposition = "outside",
            decreasing = {"marker":{"color":pwc_colours['red']}},
            increasing = {"marker":{"color":pwc_colours['orange']}},
            totals = {"marker":{"color":pwc_colours['pink']}},
            y = [i*j for i,j in zip([1,1,-1,1,-1,1,1], data[(data['Year']==year) & (data['Portfolio Basis']==portfolio) & (data['ALM Basis']==basis) & (data['Quantile']==scenario)]['Value'].to_list())],
            connector = {"line":{"color":"rgb(63, 63, 63)"}}, 
        ))

    fig.update_traces(width=0.5, hovertemplate="%{x}: %{y:$.2s}<extra></extra>", selector=dict(type='waterfall'))
    
    fig.update_layout(
            showlegend = False,
            template = 'plotly_white',
    )
    return fig

def bullet_KPIs(data, year, portfolio, basis, scenario, old_val_list):
    fig_list = []
    for i, val in enumerate(old_val_list):
        value = data[(data['Waterfall Element']==i) & (data['Year']==year) & (data['Portfolio Basis']==portfolio) & (data['ALM Basis']==basis) & (data['Quantile']==scenario)]['Value'].to_list()[0]
        fig = go.Figure(go.Indicator(
            mode = "number+delta",
            delta = {'reference': val},
            number = {'prefix': "£", 'font': {'color': website_colors['grey']}},
            value = value,
            domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
            title = {'text': f"<span style='font-size:0.7em'><b>{waterfall_name_dict[i]}</b></span>", 'font': {'color': website_colors['dark grey']}}
        ))
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        fig_list.append(fig)
    
    return fig_list

# APP LAYOUT ------------------------------------------------------
# HEADER ----------------------------------------------------------
layout_header = html.Div(children=[
    dbc.Container(
        html.H4(children='Return on capital'), className="ml-2"
    ),
])

# BODY ------------------------------------------------------------
layout = html.Div(children=[
    # Graphs
    html.Hr(style={"height": "3px", "border": "none", "background-color": website_colors['light grey']}), 
    
    dbc.Container(fluid=True,children=
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            style={'height': '70vh'},
                            id='waterfall-graph',
                            config={'displayModeBar': False},
                        )
                    , width=9),
                    dbc.Col(style={'border-left': '3px solid ' + website_colors['light grey']},
                        children = [
                            dcc.Graph(
                                style={'width': '20vw', 'height': '10vh'},
                                id='KPI-premium-tp',
                                config={'displayModeBar': False},
                                className = 'card-KPI'
                            ),
                            html.Div(),
                            dcc.Graph(
                                style={'width': '20vw', 'height': '10vh'},
                                id='KPI-unwinding-bo',
                                config={'displayModeBar': False},
                                className = 'card-KPI'
                            ),
                            html.Div(),
                            dcc.Graph(
                                style={'width': '20vw', 'height': '10vh'},
                                id='KPI-return-bo',
                                config={'displayModeBar': False},
                                className = 'card-KPI'
                            ),
                            html.Div(),
                            dcc.Graph(
                                style={'width': '20vw', 'height': '10vh'},
                                id='KPI-capital-buffer',
                                config={'displayModeBar': False},
                                className = 'card-KPI'
                            ),
                            html.Div(),
                            dcc.Graph(
                                style={'width': '20vw', 'height': '10vh'},
                                id='KPI-repayment-capital',
                                config={'displayModeBar': False},
                                className = 'card-KPI'
                            ),
                            html.Div(),
                            dcc.Graph(
                                style={'width': '20vw', 'height': '10vh'},
                                id='KPI-benefits-paid',
                                config={'displayModeBar': False},
                                className = 'card-KPI'
                            ),
                            html.Div(),
                            dcc.Graph(
                                style={'width': '20vw', 'height': '10vh'},
                                id='KPI-return-capital',
                                config={'displayModeBar': False},
                                className = 'card-KPI'
                            ),
                        ]
                    , width=3)
                ]
            , no_gutters=True)
        ]
    ),
    # Hidden div inside the app that stores the base case values
    html.Div(id='base-value', style={'display': 'none'}),
])

# APP CALLBACKS ------------------------------------------------------
# GRAPHS
@app.callback(
    Output('waterfall-graph', 'figure'),
    [Input('year-select', 'value'), 
    Input('portfolio-select', 'value'), 
    Input('ALM-select', 'value'), 
    Input('quantile-select', 'value'),]
)
def update_graph(year, portfolio, basis, scenario):
    return waterfall_filter(waterfall_df, year, portfolio, basis, scenario)

# KPIS
@app.callback(
    [Output('KPI-premium-tp', 'figure'),
    Output("KPI-unwinding-bo", "figure"),
    Output("KPI-return-bo", "figure"),
    Output("KPI-capital-buffer", "figure"),
    Output("KPI-repayment-capital", "figure"),
    Output("KPI-benefits-paid", "figure"),
    Output("KPI-return-capital", "figure")],
    [Input('year-select', 'value'), 
    Input('portfolio-select', 'value'), 
    Input('ALM-select', 'value'), 
    Input('quantile-select', 'value'),
    Input('base-value', 'children')]
)
def update_KPI(year, portfolio, basis, scenario, old_val_list):
    return bullet_KPIs(waterfall_df, year, portfolio, basis, scenario, old_val_list)

# BASE DATA
@app.callback(
    Output('base-value', 'children'),
    [Input('year-select', 'value'), 
    Input('portfolio-select', 'value'), 
    Input('ALM-select', 'value'), 
    Input('quantile-select', 'value'),]
)
def update_base_data(year, portfolio, basis, scenario):
    data = waterfall_df
    return data[(data['Year']==7) & (data['Portfolio Basis']==0) & (data['ALM Basis']==0) & (data['Quantile']==1)]['Value'].to_list()

# For single page view only
# if __name__ == '__main__':
#     app.run_server(debug=True)
