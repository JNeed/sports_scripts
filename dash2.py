from dash import Dash, dcc, html, Input, Output
from db.db import get_table
import pandas as pd
import numpy as np


df = get_table('player', 'sqlite:///db/nba.db')
teams = np.sort(df.TEAM.unique())

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(teams, id='demo-dropdown'),
    html.Div(id='dd-output-container'),
    dcc.Dropdown(options=[], id='Players')
],style = {'width':'25%'})


@app.callback(
    Output('Players','options'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    players = df.query('TEAM == @value').NAME
    return players
    
app.run_server(debug=True)
