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


# GRAPH FUNCTS --------------------------------------------------------
def waterfall_filter(data, year, portfolio, basis, scenario):
    fig = go.Figure(go.Waterfall(
            measure = ["relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x = ["Premium TP", "Unwinding of Buyout", "Return of Buyout", "Capital Buffer", "Repayment of Capital", "Benefits Paid", "Return on Capital in"],
            textposition = "outside",
            #text = ["+60", "+80", "", "-40", "-20", "Total"],
            y = [i*j for i,j in zip([1,1,-1,1,-1,1,1], data[(data['Year']==year) & (data['Portfolio Basis']==portfolio) & (data['ALM Basis']==basis) & (data['Quantile']==scenario)]['Value'].to_list())],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))

    fig.update_traces(width=0.5, hovertext='a', hovertemplate="%{x}: %{y:$.2s}<extra></extra>", selector=dict(type='waterfall'))
    
    fig.update_layout(
            showlegend = False,
            #height="90vh",
    )
    return fig

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
                    value=0,
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
                style={'width': '75vw', 'height': '80vh'},
                id='waterfall-graph',
                config={'displayModeBar': False}
            ),
            html.Div(style={'border-left': '3px solid #d3d3d3', 'height': '77vh', 'width': '3px', 'z-index': 10}),
            html.Div(
                style={
                "display": "grid",
                "gridTemplateRows": "10% 4% 10% 4% 10% 4% 10% 4% 10% 4% 10% 4% 10% 4%",
                },
                children = [
                    dbc.Card(
                        [
                        dbc.CardHeader("Premium TP"),
                        dbc.CardBody("This is some text within a card body")
                        ],
                        id='KPI-premium-tp',
                        className="card-title",
                        color="primary",
                        outline=True,
                    ),
                    html.Div(),
                    dbc.Card(
                        [
                        dbc.CardHeader("Unwinding of Buyout"),
                        dbc.CardBody("This is some text within a card body")
                        ],
                        id='KPI-unwinding-bo',
                        className="card-title",
                        color="primary",
                        outline=True,
                    ),
                    html.Div(),
                    dbc.Card(
                        [
                        dbc.CardHeader("Return of Buyout"),
                        dbc.CardBody("This is some text within a card body")
                        ],
                        id='KPI-return-bo',
                        className="card-title",
                        color="primary",
                        outline=True,
                    ),
                    html.Div(),
                    dbc.Card(
                        [
                        dbc.CardHeader("Capital Buffer"),
                        dbc.CardBody("This is some text within a card body")
                        ],
                        id='KPI-capital-buffer',
                        className="card-title",
                        color="primary",
                        outline=True,
                    ),
                    html.Div(),
                    dbc.Card(
                        [
                        dbc.CardHeader("Repayment of Capital"),
                        dbc.CardBody("This is some text within a card body")
                        ],
                        id='KPI-repayment-capital',
                        className="card-title",
                        color="primary",
                        outline=True,
                    ),
                    html.Div(),
                    dbc.Card(
                        [
                        dbc.CardHeader("Benefits Paid"),
                        dbc.CardBody("This is some text within a card body")
                        ],
                        id='KPI-benefits-paid',
                        className="card-title",
                        color="primary",
                        outline=True,
                    ),
                    html.Div(),
                    dbc.Card(
                        [
                        dbc.CardHeader("Return on Capital in"),
                        dbc.CardBody("This is some text within a card body")
                        ],
                        id='KPI-return-capital',
                        className="card-title",
                        color="primary",
                        outline=True,
                    ),
                ]
            )
        ]
    )
])

# APP CALLBACKS ------------------------------------------------------
# SLICER HEADERS
@app.callback(
    Output("year-slicer-header", "children"),
    [Input('year-select', 'value')]
)
def update_year_value(value):
    return "Year: " + str(value)

# KPIs
@app.callback(
    [Output("KPI-premium-tp", "children"),
    Output("KPI-unwinding-bo", "children"),
    Output("KPI-return-bo", "children"),
    Output("KPI-capital-buffer", "children"),
    Output("KPI-repayment-capital", "children"),
    Output("KPI-benefits-paid", "children"),
    Output("KPI-return-capital", "children")],
    [Input('year-select', 'value'), 
    Input('portfolio-select', 'value'), 
    Input('ALM-select', 'value'), 
    Input('quantile-select', 'value')]
)
def update_KPIs(year, portfolio, basis, scenario):
    data = waterfall_df
    f_d=data[(data['Year']==year) & (data['Portfolio Basis']==portfolio) & (data['ALM Basis']==basis) & (data['Quantile']==scenario)]['Value'].to_list()
    return ["{:.0f}".format(i) for i in f_d]




# GRAPHS
@app.callback(
    Output('waterfall-graph', 'figure'),
    [Input('year-select', 'value'), 
    Input('portfolio-select', 'value'), 
    Input('ALM-select', 'value'), 
    Input('quantile-select', 'value')]
)
def update_graph(year, portfolio, basis, scenario):
    return waterfall_filter(waterfall_df, year, portfolio, basis, scenario)

if __name__ == '__main__':
    app.run_server(debug=True)