import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# CSS STYLING -------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
            #text = ["+60", "+80", "", "-40", "-20", "Total"],
            y = [i*j for i,j in zip([1,1,-1,1,-1,1,1], data[(data['Year']==year) & (data['Portfolio Basis']==portfolio) & (data['ALM Basis']==basis) & (data['Quantile']==scenario)]['Value'].to_list())],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))

    fig.update_traces(width=0.5, hovertext='a', hovertemplate="%{x}: %{y:$.2s}<extra></extra>", selector=dict(type='waterfall'))
    
    fig.update_layout(
            showlegend = False,
    )
    return fig

def bullet_KPIs(data, year, portfolio, basis, scenario, old_val_list):
    fig_list = []
    for i, val in enumerate(old_val_list):
        value = data[(data['Waterfall Element']==i) & (data['Year']==year) & (data['Portfolio Basis']==portfolio) & (data['ALM Basis']==basis) & (data['Quantile']==scenario)]['Value'].to_list()[0]
        fig = go.Figure(go.Indicator(
            mode = "number+delta",
            delta = {'reference': val},
            number = {'prefix': "£"},
            value = value,
            domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
            title = {'text': waterfall_name_dict[i]}))
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        fig_list.append(fig)
    
    return fig_list

# APP LAYOUT ------------------------------------------------------
app.layout = html.Div(children=[
    # Header
    html.H1(children='Project King'),
    # Subheader
    html.H4(children='Return on capital.'),

    # Slicers
    html.Div(
        style={
        "display": "grid",
        "gridTemplateColumns": "5% 19% 5% 19% 5% 19% 5% 19%",
        },
        children=[
            html.Div(),
            html.Div(
                children=[
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
            html.Div(),
            html.Div(
                children=[
                    html.Label('Portfolio:', id='portfolio-slicer-header'),
                    dcc.Dropdown(
                    id='portfolio-select',
                    options=[
                        {'label': 'Simple Investment Strategy', 'value': 0},
                        {'label': 'Credit Investment Strategy', 'value': 1},
                        {'label': 'Agressive Investment Strategy', 'value': 2},
                    ],
                    value=0,
                    searchable=False,
                    clearable=False,
                    )
                ],
            ),
            html.Div(),
            html.Div(
                children=[
                    html.Label('ALM Basis:', id='ALM-slicer-header'),
                    dcc.Dropdown(
                    id='ALM-select',
                     options=[
                        {'label': 'BO Base', 'value': 0},
                        {'label': 'BO Downside', 'value': 1},
                    ],
                    value=0,
                    searchable=False,
                    clearable=False,
                    )
                ],
            ),
            html.Div(),
            html.Div(
                children=[
                    html.Label('Scenario:', id='quantile-slicer-header'),
                    dcc.Dropdown(
                    id='quantile-select',
                     options=[
                        {'label': 'Upside', 'value': 0},
                        {'label': 'Base', 'value': 1},
                        {'label': 'Downside', 'value': 2},
                        {'label': 'Severe Downside', 'value': 3},
                    ],
                    value=1,
                    searchable=False,
                    clearable=False,
                    )
                ],
            ),
        ],
    ),
    html.Hr(style={"height": "3px", "border": "none", "background-color": "#d3d3d3"}), 
    html.Div(
        style={
        "display": "grid",
        "gridTemplateColumns": "77% 1% 22%",
        },
        children = [
            dcc.Graph(
                style={'width': '75vw', 'height': '77vh'},
                id='waterfall-graph',
                config={'displayModeBar': False}
            ),
            html.Div(style={'border-left': '3px solid #d3d3d3', 'height': '77vh', 'width': '3px', 'z-index': 10}),
            html.Div(
                style={
                "display": "grid",
                "gridTemplateRows": "5% 9.5% 5% 9.5% 5% 9.5% 5% 9.5% 5% 9.5% 5% 9.5% 5% 9.5% 5% 9.5% ",
                },
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
            )
        ]
    ),
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])

# APP CALLBACKS ------------------------------------------------------
# SLICER HEADERS
@app.callback(
    Output("year-slicer-header", "children"),
    [Input('year-select', 'value')]
)
def update_year_value(value):
    return "Year: " + str(value)

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
    Input('intermediate-value', 'children')]
)
def update_KPI(year, portfolio, basis, scenario, old_val_list):
    return bullet_KPIs(waterfall_df, year, portfolio, basis, scenario, old_val_list)

# HIDDEN DATA
@app.callback(
    Output('intermediate-value', 'children'),
    [Input('year-select', 'value'), 
    Input('portfolio-select', 'value'), 
    Input('ALM-select', 'value'), 
    Input('quantile-select', 'value'),]
)
def update_hidden_data(year, portfolio, basis, scenario):
    data = waterfall_df
    return data[(data['Year']==7) & (data['Portfolio Basis']==0) & (data['ALM Basis']==0) & (data['Quantile']==1)]['Value'].to_list()

if __name__ == '__main__':
    app.run_server(debug=True)