# A longer file, more like a PDF with dynamic graphs and paragraphs of text that update based on selections.
# This will be a tool for selecting portfolio design based on various metrics

import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import os
import datetime

from app import app

# CONTENT ---------------------------------------------------------
# DATA ---------------------------------------------------------
#tickers = pdr.nasdaq_trader.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)[['Security Name']].reset_index()
tickers = pd.read_csv('./Data/NASDAQ.csv')[['Symbol', 'Name']]
tickers.columns = ['value', 'label']
tickers = tickers.to_dict('records')

# Calculated from obtained data
def calc_sharpe(df):
    #TODO get a correct RFR rather than 2%
    rfr = (1.02**(1/250))-1 
    df = pd.read_json(df)
    df = df.pct_change()
    vol = df.std()
    e_r = df.mean()
    sharpe = (e_r-rfr)/vol # Assumed RFR of 0%
    return list(df.columns), vol.to_list(), sharpe.to_list()

# TEXT ---------------------------------------------------------
def text1(*args):
    text = [
    f'''
    The graph on the right shows the returns for any ticker on the NASDAQ exchange.
    The slider can be used to select the date range for which you wish to see returns, 
    the earliest date visible is either, 1st Jan 2010, or the earliest the ticker appeared on NASDAQ,
    whichever is earlier.
    \n
    We can now perform some rudimentry analysis on the risk-reward for these stocks.
    * The std(s) of the stock(s) ({', '.join(args[0])}) are {', '.join([str(i) for i in args[1]])}
    * The Sharpe ratio(s) for the stock(s) ({', '.join(args[0])}) are {', '.join([str(i) for i in args[2]])}
    '''
    ]
    return text

# GRAPHS ---------------------------------------------------------

def return_graph(df: str, drawdown: bool):
    """Returns the stock returns for a list of tickers

    Args:
        df (str): json representation of pd.dataframe
        drawdown (bool): Display the drawdown graph

    Returns:
        Figure: A graph shoing the returns for the list of tickers
    """
    # Convert json to pd.Dataframe
    df = pd.read_json(df)
    #print()
    # Case where nothing is selected
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            showlegend = True,
            template = 'plotly_white',
        )
        return fig
    # Create a list of series
    ticker_series_list = [(1+df.pct_change()).cumprod()[t] for t in df.columns]
    ticker_series_max_list = [(1+df.pct_change()).cumprod().cummax()[t] for t in df.columns]
    # Create the figure
    fig = go.Figure()
    # Loop over all tickers and work out returns over the timeframe and create line plots
    for i, series in enumerate(ticker_series_list):
        fig.add_trace(go.Scatter(
            x=series.index,
            y=series,
            mode='lines',
            name=series.name,
        ))
        if drawdown:
            fig.add_trace(go.Scatter(
                x=ticker_series_max_list[i].index,
                y=ticker_series_max_list[i],
                mode='lines',
                name=series.name,
            ))
    # Change the template to be cleaner
    fig.update_layout(
            showlegend = True,
            template = 'plotly_white',
    )
    return fig


min_date = 1262304000 # 01-01-2010 unix timestamp
min_slicer_date = 1577836800 # 01-01-2020 unix timestamp
max_date = int(datetime.datetime.now().timestamp())
def get_ticker_data(ticker_list: list, date_range: list):
    """Returns the stock returns for a list of tickers

    Args:
        ticker_list (list): List of tickers to get the returns for
        date_selection (list): Date range for the x axis

    Returns:
        DataFrame: Stock relative values for 1 nominal
    """
    # Case where nothing is selected
    if ticker_list == []:
        return pd.DataFrame()
    # Convert to pandas datetime
    start = pd.to_datetime(date_range[0], unit='s', origin='unix')
    end = pd.to_datetime(date_range[1], unit='s', origin='unix')
    # Get data and convert we only take close data.
    return pdr.data.DataReader(ticker_list, 'yahoo', start , end)['Close']

# APP LAYOUT ------------------------------------------------------
# HEADER ----------------------------------------------------------
layout_header = html.Div(children=[
    dbc.Container(
        html.H4(children='The stochastic investment model'), className="ml-2"
    ),
])

# BODY ------------------------------------------------------------
layout = html.Div(children=
    [
        dcc.Store(id='ticker-data'),
        dbc.Container(fluid=True,children=
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Markdown(id='text1'),
                            width=4,
                            className='text'
                        ),
                        dbc.Col(children=
                            [
                                dcc.Graph(
                                    id='returns-graph',
                                    config={'displayModeBar': False},
                                ), 
                                dcc.RangeSlider(
                                    id='date-slider',
                                    min=min_date, # the first date
                                    max=max_date, # the last date
                                    value=[min_slicer_date, max_date],
                                    step=2592000,
                                    marks = {int(i): {'label': datetime.datetime.fromtimestamp(i).strftime("%Y")} for i in np.linspace(min_date,max_date,6)}
                                ),
                                dbc.Row(children=
                                    [
                                        dbc.Col(children=
                                            [
                                                dcc.Dropdown(
                                                    options=tickers,
                                                    id='ticker-dropdown',
                                                    multi=True
                                                ),
                                            ],
                                            width=10
                                        ),
                                        dbc.Col(children=
                                            [
                                                dcc.Checklist(
                                                    id='drawdown-check',
                                                    options=[
                                                        {'label': 'Drawdown', 'value': 'On'},
                                                    ],
                                                    value=['On']
                                                )
                                            ],
                                            width=2
                                        ),
                                    ]
                                ),
                            ],
                            width=8
                        ),     
                    ]
                ),
            ]
        ),
    ]
)


# APP CALLBACKS ------------------------------------------------------
@app.callback(    
    Output('ticker-data', 'data'),
    [Input('ticker-dropdown', 'value'),
    Input('date-slider', 'value')], 
)
def filter_tickers_and_date(ticker_list, date_selection):
    if ticker_list is None:
        ticker_list = []
    return get_ticker_data(ticker_list, date_selection).to_json()

@app.callback(
    Output('returns-graph', 'figure'),
    [Input('ticker-data', 'data'), 
    Input('drawdown-check', 'value')], 
)
def update_graph(df, drawdown):
    return return_graph(df, drawdown)

@app.callback(
    Output('text1', 'children'),
    [Input('ticker-data', 'data')], 
)
def update_text1(df):
    stock_names, var, sharpe = calc_sharpe(df)
    return text1(stock_names, var, sharpe)