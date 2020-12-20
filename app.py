import dash
import dash_bootstrap_components as dbc

# CSS STYLING -------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True
