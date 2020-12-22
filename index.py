import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app import app, server

# import all pages in the app
from apps import slicers, return_on_capital, alm

# Colour Scheme -------------------------------------------------------
pwc_colours = {'red': '#AD1B02','dark orange': '#D85604','orange': '#E88D14','yellow': '#F3BE26','pink': '#E669A2'}
website_colors = {'grey': '#7E7E7E', 'light grey': '#d3d3d3', 'dark grey': '#333333'}

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Return on Capital", href="/RoC"),
        dbc.DropdownMenuItem("ALM", href="/ALM"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Project King", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                    
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    , fluid=True),
    color=website_colors['grey'],
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# LAYOUT ------------------------------------------------------------
app.layout = html.Div([
    navbar,
    html.Div(id='page-header'),
    html.Div(id='slicers'),
    html.Div(id='page-content'),
    dcc.Location(id='url', refresh=False),
    # Hidden div inside the app that stores the slicer values
    dcc.Store(id='slicer-values', data=7),
])


# CALLBACKS ---------------------------------------------------------
# PAGE HEADER --------------------
@app.callback(Output('page-header', 'children'),
              [Input('url', 'pathname')])
def display_page_header(pathname):
    if pathname == '/RoC':
        return return_on_capital.layout_header
    elif pathname == '/ALM':
        return alm.layout_header
    else:
        return return_on_capital.layout_header

# SLICERS --------------------
@app.callback(Output('slicers', 'children'),
              [Input('url', 'pathname')])
def display_slicers(pathname):
    if pathname == '/RoC':
        return slicers.slicer_row([1,1,1,1])
    elif pathname == '/ALM':
        return slicers.slicer_row([0,1,1,0])
    else:
        return slicers.slicer_row([1,1,1,1])

# PAGE CONTENT --------------------
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/RoC':
        return return_on_capital.layout
    elif pathname == '/ALM':
        return alm.layout
    else:
        return return_on_capital.layout

# YEAR SLICER HEADERS
@app.callback(
    Output("year-slicer-header", "children"),
    [Input('year-select', 'value')]
)
def update_year_value(value):
    return "Year: " + str(value)
if __name__ == '__main__':
    app.run_server(debug=True)