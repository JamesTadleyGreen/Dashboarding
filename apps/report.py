# A longer file, more like a PDF with dynamic graphs and paragraphs of text that update based on selections.

import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app

# CONTENT ---------------------------------------------------------
# DATA ---------------------------------------------------------
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
fig1 = px.scatter(random_df, x="A", y='index')
print(random_df)

graph2 = []




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
                            className='text'),
                        dcc.Graph(
                            figure=fig1,
                            style={'width': '49vw'}, # Set this to be just below half view width so it appears next to text
                            id='graph1',
                            config={'displayModeBar': False},
                        ),      
                    ]
                ),
            ]
        ),
    ]
)


# APP CALLBACKS ------------------------------------------------------
