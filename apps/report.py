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
random_df = pd.DataFrame(np.random.randint(0,100,size=(100, 1)), columns=list('A')).reset_index()


# TEXT ---------------------------------------------------------
para1 = [
    '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
    Etiam faucibus nibh in auctor viverra. Vestibulum volutpat dolor et magna hendrerit, 
    eget aliquam arcu viverra. Nam turpis tortor, pulvinar ut bibendum nec, semper non ligula. 
    Etiam ante quam, dictum vitae orci mollis, tempus vehicula mi. In aliquam, erat faucibus lacinia scelerisque, 
    magna nibh bibendum nulla, vitae pellentesque mi nunc non nibh. Donec at mattis urna. Maecenas lorem sapien, 
    dictum at ultricies vel, luctus vitae diam. Donec nec tempor est. Etiam pellentesque vestibulum neque, 
    sit amet ullamcorper justo elementum sed.'''
]

para2 = [
    '''Morbi placerat sed quam eget dignissim. Maecenas vitae sapien sapien. 
    Ut blandit lorem vel viverra eleifend. Phasellus semper condimentum ante ut venenatis. 
    Aenean augue neque, feugiat in pulvinar aliquam, tristique sed tortor. 
    Proin vulputate a lorem vel tempus. Nullam nec arcu quam. Curabitur tempus volutpat augue, 
    nec aliquam leo finibus at. In consectetur velit risus. Sed malesuada commodo libero, 
    a mollis ante semper vel. Sed id risus varius, facilisis enim sed, vehicula lectus. 
    Praesent semper non erat id porttitor. Aenean nec elementum odio.'''
]

para3 = [
    '''Fusce in congue ipsum. Etiam ornare ut neque non sagittis. 
    Integer ut est a magna faucibus posuere. Fusce in libero et ex 
    imperdiet blandit ac ultrices nunc. Etiam ultricies ipsum eget arcu laoreet pharetra. 
    Integer ac consectetur ligula. Vivamus ultrices mauris sem, luctus molestie tellus cursus vitae. 
    Donec convallis egestas ipsum et vulputate. Pellentesque habitant morbi tristique 
    senectus et netus et malesuada fames ac turpis egestas. Nulla luctus mi sed justo mattis vulputate. 
    In vel quam auctor, feugiat justo et, varius eros.'''
]

# GRAPHS ---------------------------------------------------------
min_date = 1262304000 # 01-01-2010 unix timestamp
min_slicer_date = 1577836800 # 01-01-2020 unix timestamp
max_date = int(datetime.datetime.now().timestamp())
def return_graph(ticker_list: list, date_range: list):
    """Returns the stock returns for a list of tickers

    Args:
        ticker_list (list): List of tickers to get the returns for
        date_selection (list): Date range for the x axis

    Returns:
        Figure: A graph shoing the returns for the list of tickers
    """
    # Case where nothing is selected
    if ticker_list == []:
        fig = go.Figure()
        fig.update_layout(
            showlegend = True,
            template = 'plotly_white',
        )
        return fig
    # Convert to pandas datetime
    start = pd.to_datetime(date_range[0], unit='s', origin='unix')
    end = pd.to_datetime(date_range[1], unit='s', origin='unix')
    # Get data and convert we only take close data.
    df = pdr.data.DataReader(ticker_list, 'yahoo', start , end)['Close']
    first_date_df = df.apply(pd.Series.first_valid_index)
    # Create a list of series
    ticker_series_list = [df[t] for t in ticker_list]
    # Create the figure
    fig = go.Figure()
    # Loop over all tickers and work out returns over the timeframe and create line plots
    for series in ticker_series_list:
        series = series/series[first_date_df[series.name]]
        series = series.fillna(1)
        fig.add_trace(go.Scatter(
            x=series.index,
            y=series,
            mode='lines',
            name=series.name,
        ))
    # Change the template to be cleaner
    fig.update_layout(
            showlegend = True,
            template = 'plotly_white',
    )
    return fig

fig1 = px.scatter(random_df, x="A", y='index')

fig2 = px.scatter(random_df, x="A", y='index')




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
        dbc.Container(fluid=True,children=
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Markdown(para1[0]*3),
                            width=6,
                            className='text'
                        ),
                        dbc.Col(children=
                            [
                                dcc.Graph(
                                    #style={'width': '48vw'}, # Set this to be just below half view width so it appears next to text
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
                                dcc.Dropdown(
                                    options=tickers,
                                    id='ticker-dropdown',
                                    multi=True
                                ),
                                
                            ],
                            width=6
                        ),     
                    ]
                ),
            ]
        ),
    ]
)


# APP CALLBACKS ------------------------------------------------------
@app.callback(
    Output('returns-graph', 'figure'),
    [Input('ticker-dropdown', 'value'),
    Input('date-slider', 'value')], 
)
def update_graph(ticker_list, date_selection):
    if ticker_list is None:
        ticker_list = []
    return return_graph(ticker_list, date_selection)