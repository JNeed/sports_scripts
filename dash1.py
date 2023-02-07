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
    # dcc.Dropdown(players)
],style = {'width':'25%'})


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):

    return f'You have selected {value}'
    
app.run_server(debug=True)
