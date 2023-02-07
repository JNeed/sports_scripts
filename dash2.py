from dash import Dash, dcc, html, Input, Output
from db.db import get_table
import pandas as pd
import numpy as np
import plotly.express as px
from web_scraping import main_web

df = get_table('player', 'sqlite:///db/nba.db')
teams = np.sort(df.TEAM.unique())

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(teams, id='teams'),
    html.Div(id='dd-output-container'),
    dcc.Dropdown(options=[], id='players'),
    # dcc.Dropdown(options=[], multi = True, id='players'),
    dcc.Graph(id = 'graph')
],style = {'width':'25%'})


@app.callback(
    Output('players','options'),
    Input('teams', 'value')
)
def update_output(value):
    players = df.query('TEAM == @value').NAME
    return players

@app.callback(
    Output('graph','figure'),
    Input('players','value')
)

def update_graph(p):
    player = main_web(p, 2023)
    player.Date = pd.to_datetime(player['Date']).dt.to_period('d')
    player.PTS = player['PTS'].astype('int32')
    fig = px.scatter(player, 'Date','PTS')
    return fig
    # x = pd.to_datetime(table['Date']).dt.to_period('d')
    # y = table['PTS'].astype('int32')
app.run_server(debug=True)
